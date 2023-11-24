# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 17:38:44 2023
@author: Joe G.
"""

from machine import Pin, SoftI2C
import ssd1306py as lcd
import time
import sys

# ESP32 Pin assignment 
oled_width = 128
oled_height = 64
scl = 22
sda = 21

lcd.init_i2c(scl, sda, oled_width, oled_height)

lcd.contrast(100)  # max contrast is 255
lcd.text('Font 8x8', 0, 0, 8)
lcd.text('Font 16x16', 0, 10, 16)
lcd.text('Font 24x24', 0, 30, 24)
lcd.show()
time.sleep(5)

lcd.text('Font 32x32', 0, 0, 32)
lcd.show()
time.sleep(5)

lcd.rotate(2)
time.sleep(5)

lcd.clear()



