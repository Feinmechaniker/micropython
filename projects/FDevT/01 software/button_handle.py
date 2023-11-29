# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 08:24:08 2023

@author: Joe Grabow (grabow@amesys.de)
"""
__version__ = '1.0'
__author__ = 'Joe Grabow'

from machine import Pin, Timer

class ButtonHandler:
    def __init__(self, button_pins, debounce_delay=250):  # Debounce-Time 250 ms
        self.buttons = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in button_pins]
        self.debounce_timer = Timer(-1)
        self.button_click = 0  # default = 0, no Button Click

        for button, button_number in zip(self.buttons, range(1, len(button_pins) + 1)):
            button.irq(trigger=Pin.IRQ_FALLING, handler=self.button_interrupt_handler(button_number, debounce_delay))

    def on_pressed(self, button_number):
        self.button_click = button_number

    def button_interrupt_handler(self, button_number, debounce_delay):
        def handler(pin):
            self.debounce_timer.init(mode=self.debounce_timer.ONE_SHOT, period=debounce_delay, callback=lambda t: self.on_pressed(button_number))
        return handler

"""
Interface Demo
button_pins = [32, 33, 25]
button_handler = ButtonHandler(button_pins)

# mainloop
while True:
    if button_handler.button_click != 0:  # Button Click 
        print(str(button_handler.button_click))
        button_handler.button_click = 0  # Reset Button
"""
