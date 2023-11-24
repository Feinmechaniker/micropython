## MicroPython driver for SSD1306 OLED displays.

This driver is based on the SSD1306 driver from Adafruit. It is extended by the fonts
* 16x16
* 24x24
* 32x32

## API
```python
def init_i2c(scl, sda, width, height):
def clear():
def show():
def pixel(x, y):
def contrast(contrast):
def invert(invert):
def rotate(rotate):
def text(string, x_axis, y_axis, font_size):
```

## example 1
```python
# ESP32 Pin assignment
scl = 22
sda = 21

## SSD1306
oled_width = 128
oled_height = 64


lcd.init_i2c(scl, sda, oled_width, oled_height)

lcd.contrast(100)  # max contrast is 255
lcd.text('Font 8x8', 0, 0, 8)
lcd.text('Font 16x16', 0, 10, 16)
lcd.text('Font 24x24', 0, 30, 24)
lcd.show()
```
![example 1](/Feinmechaniker/micropython/tree/main/drivers/ssd1306/image)/figure_1.png")

## example 2
```python
lcd.text('Font 32x32', 0, 0, 32)
lcd.show()
```
![example 2](figure_2.png "Image Title")

## example 3
```python
lcd.rotate(2)
```
![example 3](figure_3.png "Image Title")

