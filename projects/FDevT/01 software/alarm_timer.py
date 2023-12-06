# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 08:24:08 2023

@author: Grabow
"""
__version__ = '1.0'
__author__ = 'Joe Grabow'

from machine import Timer, Pin
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


    motor_pin = 2  # GPIO-Pin H-Bridge Change
    motor = Pin(motor_pin, Pin.OUT)

    def __init__(self):
        """Initialize the CountdownTimer."""
        self.timer = Timer(0)  # use Timer 0
        self.alarm_set = self.ALARM_OFF
        self.sec_before = 5
        self.is_initialized_0 = False
        self.is_initialized_1 = False


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
        self.is_initialized_0 = True   
        self.timer.init(period=1000, mode=Timer.PERIODIC, callback=self.timer_callback)

    def pause_timer(self):
        """Wait Timer."""        
        if self.is_initialized_0:
            self.is_initialized_0 = False
            self.timer.deinit()
            self.alarm_set = 1  # alarm off

    def set_beep(self, seconds_before):
        """Beep befor the timer is finished."""      
        self.sec_before = seconds_before
    
    def change_motor_on(self, change):
        
        def toggle_motor(timer):
            self.motor.value(not self.motor.value())  # changing the direction of rotation 

        self.motor_timer = Timer(1)  # use Timer 1
        
        self.is_initialized_1 = True        
        interval_ms = change * 1000
        self.motor_timer.init(period=interval_ms, mode=Timer.PERIODIC, callback=toggle_motor)

    def change_motor_off(self):
        if self.is_initialized_1:
            self.is_initialized_1 = False
            self.motor_timer.deinit()
            self.motor.value(0)


