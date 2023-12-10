# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 08:24:08 2023

@author: Grabow
"""
__version__ = '1.0'
__author__ = 'Joe Grabow'

from machine import Pin

# Debugging
debug = True

# SD-Card
MOSI = Pin(12)
MISO = Pin(13)
SCK = Pin(14)
CS = Pin(27)

SD_CARD_PATH = '/sd'
TARGET_FILE = 'default.json'

# OLED
SDA = 21
SCL = 22
OLED_WIDTH = 128 
OLED_HEIGHT = 64

# Motor
PWM_FREQUENCY = 10
PWM_PIN = 15  # GPIO-Pin for Motor Drive
MOTOR_PIN = 2  # GPIO-Pin H-Bridge Change
MOTOR_2_PIN = 16

# Beep
BEEP_PIN = 4

# Buttons
BUTTON_PINS = [32, 33, 25]  # Pin 32 is UP, Pin 33 is ENTER, Pin 25 is DOWN
