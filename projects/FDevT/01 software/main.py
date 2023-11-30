# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 08:24:08 2023

@author: Grabow
"""
__version__ = '1.0'
__author__ = 'Joe Grabow'

import ssd1306py as lcd
import ujson
from machine import Pin, Timer, SoftI2C
from button_handle import ButtonHandler
from state_machine import StateMachine
from alarm_timer import CountdownTimer

# Debugging
debug = True

# Hardware 
button_pins = [32, 33, 25]  # Pin 32 is UP, Pin 33 is ENTER, Pin 25 is DOWN

# ESP32 Pin assignment for OLED and I2C
oled_width = 128 
oled_height = 64
scl = 22
sda = 21

# all variables
# Variable set for the recipe
D_Min = 0
D_Sec = 0
S_Min = 0
S_Sec = 0
F_Min = 0
F_Sec = 0

# Oled-Menue Variable 
DEV_oled_time, STOP_oled_time, FIX_oled_time = '00:00', '00:00', '00:00'


# Initialize button handler, state machine, and countdown timer
#button_handler = ButtonHandler(button_pins)
#sm = StateMachine()
#count_timer = CountdownTimer()

# Function for initialization
def initialize():
    global button_handler, sm, count_timer

    # Initialize button handler, state machine, and countdown timer
    button_handler = ButtonHandler(button_pins)
    sm = StateMachine()
    count_timer = CountdownTimer()

# User State-Functions
def s_f_1():
    # MAIN State
    # PROCES
    # RECIPES
    if debug:
        print('State 1')
    lcd.clear()
    lcd.text('  FDevT 1.0', 0, 0, 16)
    lcd.text('> PROCESS', 0, 20, 16)
    lcd.text('  RECIPES', 0, 40, 16)
    lcd.show()

# PROCESS DEV init
def s_f_2():
    global D_Min, D_Sec, S_Min, S_Sec, F_Min, F_Sec
    global DEV_oled_time, STOP_oled_time, FIX_oled_time
    
    if debug:
        print('State 2')
    
    # load recipe
    with open('recipes.json', 'r') as file:
        data = ujson.load(file)
        
    D_Min, D_Sec = data["D_Min"], data["D_Sec"]
    S_Min, S_Sec = data["S_Min"], data["S_Sec"]
    F_Min, F_Sec = data["F_Min"], data["F_Sec"]

    # Recipe times
    DEV_oled_time = f"{D_Min:02d}:{D_Sec:02d}"
    STOP_oled_time = f"{S_Min:02d}:{S_Sec:02d}"
    FIX_oled_time = f"{F_Min:02d}:{F_Sec:02d}"
    
    count_timer.set_timer(D_Min, D_Sec)  # initialise Timer

    # OLED Display
    lcd.clear()
    lcd.text('DEVELOPER INIT', 0, 0, 16)
    lcd.text(DEV_oled_time, 0, 16, 32)
    #lcd.text('>', 115, 16, 32)  # skip
    lcd.text('<', 85,16,32)  # return
    lcd.text('#', 99,16,32)  # wait
    #lcd.text('*', 99,16,32)  # run
    lcd.text(DEV_oled_time, 0, 48, 16)
    lcd.show()


# PROCESS DEV-Timer run
def s_f_3():
    global DEV_oled_time
    
    if debug:
        print('State 3')
    
    [r_min, r_sec, t_sec] = count_timer.get_remaining_time()
    oled_time = f"{r_min:02d}:{r_sec:02d}"
    
    # OLED Menue
    lcd.clear()
    lcd.text('DEVELOPER RUN', 0, 0, 16)
    lcd.text(oled_time, 0, 16, 32)
    lcd.text('>', 115, 16, 32)  # skip
    lcd.text('<', 85,16,32)  # return
    #lcd.text('#', 99,16,32)  # wait
    lcd.text('*', 99,16,32)  # run
    lcd.text(DEV_oled_time, 0, 48, 16)
    lcd.show()
    
    count_timer.start_timer()  # DEV-Timer run    


# PROCESS DEV-Timer wait
def s_f_4():
    global DEV_oled_time
    
    if debug:
        print('State 4')
        
    count_timer.pause_timer()
    [r_min, r_sec, t_sec] = count_timer.get_remaining_time()  # determine remaining time
    oled_time = f"{r_min:02d}:{r_sec:02d}"
    
    # OLED Menue
    lcd.clear()
    lcd.text('DEVELOPER WAIT', 0, 0, 16)
    lcd.text(oled_time, 0, 16, 32)
    #lcd.text('>', 115, 16, 32)  # skip
    lcd.text('<', 85,16,32)  # return
    lcd.text('#', 99,16,32)  # wait
    #lcd.text('*', 99,16,32)  # run
    lcd.text(DEV_oled_time, 0, 48, 16)
    lcd.show()     


# PROCESS STOP init
def s_f_5():
    global STOP_oled_time
    
    if debug:
        print('State 5')
        
    count_timer.set_timer(S_Min, S_Sec)  # initialise STOP-Timer
    oled_time = f"{S_Min:02d}:{S_Sec:02d}"
    
    # Oled Menue
    lcd.clear()
    lcd.text('STOP INIT', 0, 0, 16)
    lcd.text(oled_time, 0, 16, 32)
    #lcd.text('>', 115, 16, 32)  # skip
    lcd.text('<', 85,16,32)  # return
    lcd.text('#', 99,16,32)  # wait
    #lcd.text('*', 99,16,32)  # run
    lcd.text(STOP_oled_time, 0, 48, 16)
    lcd.show()  


# PROCESS STOP-Timer run
def s_f_6():
    global STOP_oled_time
        
    if debug:
        print('State 6')
        
    [r_min, r_sec, t_sec] = count_timer.get_remaining_time()  # determine remaining time
    oled_time = f"{r_min:02d}:{r_sec:02d}"
    
    # Oled Menue
    lcd.clear()
    lcd.text('STOP RUN', 0, 0, 16)
    lcd.text(oled_time, 0, 16, 32)
    lcd.text('>', 115, 16, 32)  # skip
    lcd.text('<', 85,16,32)  # return
    #lcd.text('#', 99,16,32)  # wait
    lcd.text('*', 99,16,32)  # run
    lcd.text(STOP_oled_time, 0, 48, 16)
    lcd.show()

    count_timer.start_timer()  # STOP-Timer run   


# PROCESS STOP-Timer wait
def s_f_7():
    global STOP_oled_time
        
    if debug:
        print('State 7')
        
    count_timer.pause_timer()
    [r_min, r_sec, t_sec] = count_timer.get_remaining_time()  # determine remaining time
    oled_time = f"{r_min:02d}:{r_sec:02d}"

    # Oled Menue
    lcd.clear()
    lcd.text('STOP WAIT', 0, 0, 16)
    lcd.text(oled_time, 0, 16, 32)
    #lcd.text('>', 115, 16, 32)  # skip
    lcd.text('<', 85,16,32)  # return
    lcd.text('#', 99,16,32)  # wait
    #lcd.text('*', 99,16,32)  # run
    lcd.text(STOP_oled_time, 0, 48, 16)
    lcd.show()  


# Process FIX init
def s_f_8():
    global FIX_oled_time
        
    if debug:
        print('State 8')

    count_timer.set_timer(F_Min, F_Sec)  # initialise FIX-Timer
    oled_time = f"{F_Min:02d}:{F_Sec:02d}"

    # Oled Menue
    lcd.clear()
    lcd.text('FIX INIT', 0, 0, 16)
    lcd.text(oled_time, 0, 16, 32)
    #lcd.text('>', 115, 16, 32)  # skip
    lcd.text('<', 85,16,32)  # return
    lcd.text('#', 99,16,32)  # wait
    #lcd.text('*', 99,16,32)  # run
    lcd.text(FIX_oled_time, 0, 48, 16)
    lcd.show()  


# Process FIX run
def s_f_9():
    global FIX_oled_time
        
    if debug:
        print('State 9')
        
    [r_min, r_sec, t_sec] = count_timer.get_remaining_time()  # determine remaining time
    oled_time = f"{r_min:02d}:{r_sec:02d}"        

    # Oled Menue
    lcd.clear()
    lcd.text('FIX RUN', 0, 0, 16)
    lcd.text(oled_time, 0, 16, 32)
    lcd.text('>', 115, 16, 32)  # skip
    lcd.text('<', 85,16,32)  # return
    #lcd.text('#', 99,16,32)  # wait
    lcd.text('*', 99,16,32)  # run
    lcd.text(FIX_oled_time, 0, 48, 16)
    lcd.show()
    
    count_timer.start_timer()  # FIX-Timer run   


# PROCESS FIX-Timer wait
def s_f_10():
    global FIX_oled_time
        
    if debug:
        print('State 10')

    count_timer.pause_timer()
    [r_min, r_sec, t_sec] = count_timer.get_remaining_time()  # determine remaining time
    oled_time = f"{r_min:02d}:{r_sec:02d}"

    # Oled Menue
    lcd.clear()
    lcd.text('FIX WAIT', 0, 0, 16)
    lcd.text(oled_time, 0, 16, 32)
    #lcd.text('>', 115, 16, 32)  # skip
    lcd.text('<', 85,16,32)  # return
    lcd.text('#', 99,16,32)  # wait
    #lcd.text('*', 99,16,32)  # run
    lcd.text(FIX_oled_time, 0, 48, 16)
    lcd.show()  

def s_f_11():
    # RECIPES end
    if debug:
        print('State 11')
    
    count_timer.pause_timer()
    
    # Oled Menue    
    lcd.clear()
    lcd.text('PROCESS', 0, 0, 16)
    lcd.text('END', 0, 16, 32)
    #lcd.text('>', 115, 16, 32)  # skip
    lcd.text('<', 85,16,32)  # return
    lcd.text('#', 99,16,32)  # wait
    #lcd.text('*', 99,16,32)  # run
    lcd.show()  

# Dictionary with all State-Functions
statefunctions = {
    1: s_f_1,
    2: s_f_2,
    3: s_f_3,
    4: s_f_4,    
    5: s_f_5,
    6: s_f_6,
    7: s_f_7,
    8: s_f_8,
    9: s_f_9,
    10: s_f_10,
    11: s_f_11,
}


# mainloop
initialize()

lcd.init_i2c(scl, sda, oled_width, oled_height)
lcd.contrast(100)  # OLED-Contrast, max contrast is 255

state = 1  # Start State (PROCESS)
s_f_1()  # User-State PROCESS

while True:
    if (button_handler.button_click != 0) or (count_timer.get_alarm() == 0):  # Button Click or timer == 0
        state = sm.transition(state, 11, int(button_handler.button_click), count_timer.get_alarm())  # Trigger State-machine  
        
        if state in statefunctions:  # Call User-State-Function
            statefunctions[state]()
        else:
            print("state not defind")

        button_handler.button_click = 0  # Reset Button


