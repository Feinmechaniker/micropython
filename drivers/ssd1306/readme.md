## MicroPython driver for SSD1306 OLED displays.

This driver is based on the SSD1306 driver from Adafruit. It is extended by the fonts
* 16x16
* 24x24
* 32x32

## API
```python
def init_i2c(scl, sda, width, height:
def clear():
def show():
def pixel(x, y):
def contrast(contrast):
def invert(invert):
def rotate(rotate):
def text(string, x_axis, y_axis, font_size):
