"""
Copyright 2021-2021 The jdh99 Authors. All rights reserved.
ssd1306操作封装.支持多种英文字库
Authors: <jdh821@163.com>
forked from jdhxyy/ssd1306py-micropython
Authors: Joe G. 
"""


import ssd1306py.ssd1306 as ssd1306
import ssd1306py.ascii16 as ascii16
import ssd1306py.ascii32 as ascii32
import ssd1306py.ascii24 as ascii24
import ssd1306py.cn as cn
from machine import SoftI2C, Pin

_oled = None
_i2c = None
_width = 0
_height = 0


def init_i2c(scl, sda, width, height, i2c=-1):
    """
    :param scl: i2c
    :param sda: i2c
    :param width: oled
    :param height: oled
    :param i2c: i2c
    """
    global _oled, _width, _height
    _i2c = SoftI2C(scl=Pin(scl), sda=Pin(sda))
    _width = width
    _height = height
    _oled = ssd1306.SSD1306_I2C(_width, _height, _i2c)


def clear():
    global _oled
    _oled.fill(0)
    _oled.show()


def show():
    global _oled
    _oled.show()


def pixel(x, y):
    global _oled
    _oled.pixel(x, y, 1)


def contrast(contrast):
    global _oled
    _oled.contrast(contrast)


def invert(invert):
    global _oled
    _oled.invert(invert)
  
  
def rotate(rotate):
    global _oled
    _oled.rotate(rotate)  
  

def text(string, x_axis, y_axis, font_size):
    global _oled
    if font_size != 8 and font_size != 16 and font_size != 24 and font_size != 32:
        return

    if font_size == 8:
        _oled.text(string, x_axis, y_axis)
        return

    if font_size == 16:
        ascii16.display(_oled, string, x_axis, y_axis)
    if font_size == 24:
        ascii24.display(_oled, string, x_axis, y_axis)
    if font_size == 32:
        ascii32.display(_oled, string, x_axis, y_axis)


def set_font(font, font_size):
    cn.set_font(font, font_size)


def text_cn(string, x_axis, y_axis, font_size):
    global _oled
    cn.display(_oled, string, x_axis, y_axis, font_size)
    
