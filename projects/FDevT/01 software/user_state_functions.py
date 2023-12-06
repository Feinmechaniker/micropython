# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 08:24:08 2023

@author: Grabow
"""
__version__ = '1.0'
__author__ = 'Joe Grabow'

import ssd1306py as lcd
import ujson
from alarm_timer import CountdownTimer
import init
from machine import Pin, PWM

# Debugging
debug = True

# PWM functions
pwm_frequency = 10
pwm_pin = 15  # GPIO-Pin for Motor Drive
pwm = PWM(Pin(pwm_pin),pwm_frequency)
pwm.duty(0)  # PWM off

count_timer = CountdownTimer()  # all Timer functions

data, file_list = init.get_config()  # get 'default.json' from SD-Card or Flash-ROM

# Variable set for the recipe
D_Min, D_Sec = data["D_Min"], data["D_Sec"]
S_Min, S_Sec = data["S_Min"], data["S_Sec"]
F_Min, F_Sec = data["F_Min"], data["F_Sec"]
Speed, Change = data["Speed"], data["Change"]
pwm_speed = int((Speed / 100) * 1023) 

DEV_oled_time = f"{D_Min:02d}:{D_Sec:02d}"
STOP_oled_time = f"{S_Min:02d}:{S_Sec:02d}"
FIX_oled_time = f"{F_Min:02d}:{F_Sec:02d}"


# all User-State-Functions
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
#    global D_Min, D_Sec, S_Min, S_Sec, F_Min, F_Sec
    global DEV_oled_time, STOP_oled_time, FIX_oled_time
    
    if debug:
        print('State 2')

    count_timer.pause_timer()  # stop timer when running 
    count_timer.set_timer(D_Min, D_Sec)  # initialise Timer
    count_timer.change_motor_off()  # changing the direction of rotation off
    pwm.duty(0)  # PWM off  

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
    pwm.duty(pwm_speed)  # PWM on
    if Change != 0:
        count_timer.change_motor_on(Change)  # changing the direction of rotation on

# PROCESS DEV-Timer wait
def s_f_4():
    global DEV_oled_time
    
    if debug:
        print('State 4')
        
    count_timer.pause_timer()
    pwm.duty(0)  # PWM off    
    count_timer.change_motor_off()  # changing the direction of rotation off
    
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

    count_timer.pause_timer()  # stop timer when running 
    count_timer.set_timer(S_Min, S_Sec)  # initialise STOP-Timer
    count_timer.change_motor_off()  # changing the direction of rotation off
    pwm.duty(0)  # PWM off      
    
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
    pwm.duty(pwm_speed)  # PWM on    
    if Change != 0:
        count_timer.change_motor_on(Change)  # changing the direction of rotation on

# PROCESS STOP-Timer wait
def s_f_7():
    global STOP_oled_time
        
    if debug:
        print('State 7')
        
    count_timer.pause_timer()
    pwm.duty(0)  # PWM off    
    count_timer.change_motor_off()  # changing the direction of rotation off 
    
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
    
    count_timer.pause_timer()  # stop timer when running 
    count_timer.set_timer(F_Min, F_Sec)  # initialise FIX-Timer
    count_timer.change_motor_off()  # changing the direction of rotation off
    pwm.duty(0)  # PWM off  
    
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
    pwm.duty(pwm_speed)  # PWM on    
    if Change != 0:
        count_timer.change_motor_on(Change)  # changing the direction of rotation on

# PROCESS FIX-Timer wait
def s_f_10():
    global FIX_oled_time
        
    if debug:
        print('State 10')

    count_timer.pause_timer()
    pwm.duty(0)  # PWM off
    count_timer.change_motor_off()  # changing the direction of rotation off   
    
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
    pwm.duty(0)  # PWM off    
    count_timer.change_motor_off()  # changing the direction of rotation off 
    
    # Oled Menue    
    lcd.clear()
    lcd.text('PROCESS', 0, 0, 16)
    lcd.text('END', 0, 16, 32)
    #lcd.text('>', 115, 16, 32)  # skip
    lcd.text('<', 85,16,32)  # return
    lcd.text('#', 99,16,32)  # wait
    #lcd.text('*', 99,16,32)  # run
    lcd.show()
    
def alarm_state():
    return count_timer.get_alarm()
