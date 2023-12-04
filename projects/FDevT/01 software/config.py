# config.py

from machine import Pin, SoftSPI
import sdcard
import os
import ujson
import ssd1306py as lcd
import time

D_Min, D_Sec = 0, 0
S_Min, S_Sec = 0, 0
F_Min, F_Sec = 0, 0
Speed, Change = 0, 0

SD_CARD_PATH = '/sd'
TARGET_FILE = 'default.json'

def init_sd():
    try:
        spi = SoftSPI(1, sck=Pin(14), mosi=Pin(12), miso=Pin(13))
        sd = sdcard.SDCard(spi, Pin(27))
        os.mount(sd, SD_CARD_PATH)
    except Exception as e:
        lcd.clear()
        lcd.text('no SD-Card', 0, 0, 16)
        lcd.show()
        time.sleep(2)
        raise

def read_data_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = ujson.load(file)
        return data
    except Exception as e:
        lcd.clear()
        lcd.text(f"Error reading {file_path}: {str(e)}", 0, 0, 16)
        lcd.show()
        time.sleep(2)
        raise

def read_config():
    global D_Min, D_Sec, S_Min, S_Sec, F_Min, F_Sec, Speed, Change

    init_sd()

    try:
        # ESP32 Pin assignment for OLED and I2C
        oled_width = 128
        oled_height = 64
        scl = 22
        sda = 21
        lcd.init_i2c(scl, sda, oled_width, oled_height)

        files = os.listdir(SD_CARD_PATH)
        file_list = [os.path.join(SD_CARD_PATH, file) for file in files if os.stat(os.path.join(SD_CARD_PATH, file))[0] & 0x8000]

    except Exception as e:
        lcd.clear()
        lcd.text(f"Error: {str(e)}", 0, 0, 16)
        lcd.show()
        time.sleep(2)
        return

    sd_default_flag = 0

    # Read "default.json" from SD-Card
    for file_path in file_list:
        if file_path.endswith(TARGET_FILE):
            sd_default_flag = 1
            data = read_data_from_file(file_path)
            lcd.clear()
            lcd.text('FDevT 1.0', 0, 0, 16)
            lcd.text('SD-Card', 0, 20, 16)
            lcd.text('Configuration  ', 0, 40, 16)
            lcd.show()
            time.sleep(3)
            break

    # Read "default.json" from Flash-ROM
    if sd_default_flag == 0:
        try:
            data = read_data_from_file(TARGET_FILE)
            lcd.clear()
            lcd.text('FDevT 1.0', 0, 0, 16)
            lcd.text('Flash-ROM', 0, 20, 16)
            lcd.text('Configuration  ', 0, 40, 16)
            lcd.show()
            time.sleep(3)

        except Exception as e:
            lcd.clear()
            lcd.text(f"Error reading {TARGET_FILE} from Flash-ROM: {str(e)}", 0, 0, 16)
            lcd.show()
            time.sleep(2)
            return

    D_Min, D_Sec = data["D_Min"], data["D_Sec"]
    S_Min, S_Sec = data["S_Min"], data["S_Sec"]
    F_Min, F_Sec = data["F_Min"], data["F_Sec"]
    Speed, Change = data["Speed"], data["Change"]
