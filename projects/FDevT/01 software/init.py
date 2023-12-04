# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 08:24:08 2023

@author: Grabow
"""
__version__ = '1.0'
__author__ = 'Joe Grabow'


#import machine
from machine import Pin, SPI, SoftSPI
import sdcard
import os
import ujson
import ssd1306py as lcd
import time

SD_CARD_PATH = '/sd'
TARGET_FILE = 'default.json'

def init_sd():
    # Initialize the SD card
    # MISO pin to ESP32 GPIO13
    # MOSI pin to ESP32 GPIO12
    # SCK pin to ESP32 GPIO14
    # CS pin to ESP32 GPIO27
    spi=SoftSPI(1,sck=Pin(14),mosi=Pin(12),miso=Pin(13))
    sd=sdcard.SDCard(spi,Pin(27))

    # Create a instance of MicroPython Unix-like Virtual File System (VFS),
    vfs=os.VfsFat(sd)

    # Mount the SD card
    os.mount(sd, SD_CARD_PATH)

def read_file_list():
    file_list = []
    try:
        init_sd()
        files = os.listdir(SD_CARD_PATH)
    
        for file in files:
            # Create the complete path to the current element
            file_path = '/'.join([SD_CARD_PATH, file])
        
            # Check whether this is a file
            if os.stat(file_path)[0] & 0x8000:
                file_list.append(file_path)
    
    except Exception as e:
        #print("Error:", str(e))
        lcd.clear()
        lcd.text('no SD-Card', 0, 0, 16)
        lcd.show()
        time.sleep(2)

    return file_list

def read_default_config(file_list):
    SD_DEFAULT_FLAG = 0

    # read "default.json" form SD-Card
    for file_path in file_list:
        if file_path.endswith(TARGET_FILE):
            SD_DEFAULT_FLAG = 1
            with open(file_path, 'r') as file:  # default.json found on sd-card
                data = ujson.load(file)
                lcd.clear()
                lcd.text('FDevT 1.0', 0, 0, 16)
                lcd.text('SD-Card', 0, 20, 16)
                lcd.text('Configuration  ', 0, 40, 16)
                lcd.show()
                time.sleep(3)
            break
    
    # read "default.json" form Flash-ROM
    if SD_DEFAULT_FLAG == 0:
        with open(TARGET_FILE, 'r') as file: # default.json found on Flash-ROM
            data = ujson.load(file)
            lcd.clear()
            lcd.text('FDevT 1.0', 0, 0, 16)
            lcd.text('Flash-ROM', 0, 20, 16)
            lcd.text('Configuration  ', 0, 40, 16)
            lcd.show()
            time.sleep(3)
    
    return data
 
def oled():
    # ESP32 Pin assignment for OLED and I2C
    oled_width = 128 
    oled_height = 64
    scl = 22
    sda = 21
    lcd.init_i2c(scl, sda, oled_width, oled_height)

def get_config():
    data = []
    oled()    
    file_list = read_file_list()
    data = read_default_config(file_list)
    return data, file_list


  