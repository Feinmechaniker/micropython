# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 08:24:08 2023

@author: Grabow
"""
__version__ = '1.0'
__author__ = 'Joe Grabow'

from machine import Timer
import ssd1306py as lcd

class CountdownTimer:
    """A class for a countdown timer. The interrupt time is exactly one second"""
    ALARM_OFF = 1
    ALARM_ON = 0
    
    # ESP32 Pin assignment for OLED and I2C
    oled_width = 128 
    oled_height = 64
    scl = 22
    sda = 21
    lcd.init_i2c(scl, sda, oled_width, oled_height)

    
    def __init__(self):
        """Initialize the CountdownTimer."""
        self.timer = Timer(-1)  # next Timer
        self.alarm_set = self.ALARM_OFF
        self.sec_before = 5

    def set_timer(self, minutes, seconds):
        """Set the timer to the specified minutes and seconds."""
        self.total_seconds = minutes * 60 + seconds
        self.alarm_set = self.ALARM_OFF

    def get_remaining_time(self):
        """Remaining the CountdownTimer."""
        remaining_minutes, remaining_seconds = divmod(self.total_seconds, 60)
        return remaining_minutes, remaining_seconds, self.total_seconds

    def get_alarm(self):
        """Get Alarm Flag."""
        return self.alarm_set

    def display_time(self):
        """Displays the time on the OLED."""
        r_min, r_sec = divmod(self.total_seconds, 60)
        oled_time = f"{r_min:02d}:{r_sec:02d}"
        lcd.text(oled_time, 0, 16, 32)
        lcd.show()
        print(oled_time)

    def timer_callback(self, timer):
        """Callback for Timer-Interrupt."""
        self.total_seconds -= 1
        self.display_time()

        if self.total_seconds <= 0:
            self.timer.deinit()  # stop Timer stoppen
            self.alarm_set = self.ALARM_ON  # time has expired

        # Beep x seconds before timer ends
        elif self.total_seconds == self.sec_before:
            print("Beep")

    def start_timer(self):  # only start without changing the time
        """Start Timer."""
        print('Timer Start')
        self.timer.init(period=1000, mode=Timer.PERIODIC, callback=self.timer_callback)

    def pause_timer(self):
        """Wait Timer."""        
        self.timer.deinit()
        self.alarm_set = 1  # alarm off

    def set_beep(self, seconds_before):
        """Beep befor the timer is finished."""      
        self.sec_before = seconds_before






