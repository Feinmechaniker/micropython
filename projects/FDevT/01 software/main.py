# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 08:24:08 2023

@author: Grabow
"""
__version__ = '1.0'
__author__ = 'Joe Grabow'

import ssd1306py as lcd
from machine import Pin, Timer, SoftI2C
from button_handle import ButtonHandler
from state_machine import StateMachine

# Debugging
debug = True

# Hardware 
button_pins = [32, 33, 25]  # Pin 32 is UP, Pin 33 is ENTER, Pin 25 is DOWN

# ESP32 Pin assignment for OLED and I2C
oled_width = 128 
oled_height = 64
scl = 22
sda = 21

# use Functions and Classes
button_handler = ButtonHandler(button_pins)
sm = StateMachine()


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

def s_f_2():
    # PROCESS DEV
    # load Recipes
    # Timer = DEV
    if debug:
        print('State 2')
    lcd.clear()
    lcd.text('DEVELOPER INIT', 0, 0, 16)
    lcd.text('08:00', 0, 16, 32)
    #lcd.text('>', 115, 16, 32)  # skip
    lcd.text('<', 85,16,32)  # return
    lcd.text('#', 99,16,32)  # wait
    #lcd.text('*', 99,16,32)  # run
    lcd.text('08:00', 0, 48, 16)
    lcd.show()

def s_f_3():
    # DEV-Timer run
    if debug:
        print('State 3')
    lcd.clear()
    lcd.text('DEVELOPER RUN', 0, 0, 16)
    lcd.text('00:00', 0, 16, 32)
    lcd.text('>', 115, 16, 32)  # skip
    lcd.text('<', 85,16,32)  # return
    #lcd.text('#', 99,16,32)  # wait
    lcd.text('*', 99,16,32)  # run
    lcd.text('08:00', 0, 48, 16)
    lcd.show()        

def s_f_4():
    # DEV-Timer wait
    if debug:
        print('State 4')
    lcd.clear()
    lcd.text('DEVELOPER STOP', 0, 0, 16)
    lcd.text('00:00', 0, 16, 32)
    #lcd.text('>', 115, 16, 32)  # skip
    lcd.text('<', 85,16,32)  # return
    lcd.text('#', 99,16,32)  # wait
    #lcd.text('*', 99,16,32)  # run
    lcd.text('08:00', 0, 48, 16)
    lcd.show()     

def s_f_5():
    # Timer = STOP
    if debug:
        print('State 5')
    lcd.clear()
    lcd.text('STOP INIT', 0, 0, 16)
    lcd.text('00:30', 0, 16, 32)
    #lcd.text('>', 115, 16, 32)  # skip
    lcd.text('<', 85,16,32)  # return
    lcd.text('#', 99,16,32)  # wait
    #lcd.text('*', 99,16,32)  # run
    lcd.text('00:30', 0, 48, 16)
    lcd.show()  

def s_f_6():
    # STOP-Timer run
    if debug:
        print('State 6')
    lcd.clear()
    lcd.text('STOP RUN', 0, 0, 16)
    lcd.text('00:30', 0, 16, 32)
    lcd.text('>', 115, 16, 32)  # skip
    lcd.text('<', 85,16,32)  # return
    #lcd.text('#', 99,16,32)  # wait
    lcd.text('*', 99,16,32)  # run
    lcd.text('00:30', 0, 48, 16)
    lcd.show()  

def s_f_7():
    # STOP-Timer wait
    if debug:
        print('State 7')
    lcd.clear()
    lcd.text('STOP WAIT', 0, 0, 16)
    lcd.text('00:30', 0, 16, 32)
    #lcd.text('>', 115, 16, 32)  # skip
    lcd.text('<', 85,16,32)  # return
    lcd.text('#', 99,16,32)  # wait
    #lcd.text('*', 99,16,32)  # run
    lcd.text('00:30', 0, 48, 16)
    lcd.show()  

def s_f_8():
    # TIMER = FIX
    if debug:
        print('State 8')
    lcd.clear()
    lcd.text('FIX INIT', 0, 0, 16)
    lcd.text('04:30', 0, 16, 32)
    #lcd.text('>', 115, 16, 32)  # skip
    lcd.text('<', 85,16,32)  # return
    lcd.text('#', 99,16,32)  # wait
    #lcd.text('*', 99,16,32)  # run
    lcd.text('00:30', 0, 48, 16)
    lcd.show()  

def s_f_9():
    # FIX-Timer run
    if debug:
        print('State 9')
    lcd.clear()
    lcd.text('FIX RUN', 0, 0, 16)
    lcd.text('04:30', 0, 16, 32)
    lcd.text('>', 115, 16, 32)  # skip
    lcd.text('<', 85,16,32)  # return
    #lcd.text('#', 99,16,32)  # wait
    lcd.text('*', 99,16,32)  # run
    lcd.text('00:30', 0, 48, 16)
    lcd.show()  

def s_f_10():
    # FIX-Timer wait
    if debug:
        print('State 10')
    lcd.clear()
    lcd.text('FIX WAIT', 0, 0, 16)
    lcd.text('04:30', 0, 16, 32)
    #lcd.text('>', 115, 16, 32)  # skip
    lcd.text('<', 85,16,32)  # return
    lcd.text('#', 99,16,32)  # wait
    #lcd.text('*', 99,16,32)  # run
    lcd.text('00:30', 0, 48, 16)
    lcd.show()  

def s_f_11():
    # RECIPES end
    if debug:
        print('State 11')
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
lcd.init_i2c(scl, sda, oled_width, oled_height)
lcd.contrast(100)  # OLED-Contrast, max contrast is 255

state = 1  # Start State
s_f_1()

while True:
    if button_handler.button_click != 0:  # Button Click
        state = sm.transition(state, 11, int(button_handler.button_click), 1)  # Trigger State-machine  
        
        if state in statefunctions:  # Call User-State-Function
            statefunctions[state]()
        else:
            print("state not defind")

#        print(str(button_handler.button_click))
        button_handler.button_click = 0  # Reset Button

