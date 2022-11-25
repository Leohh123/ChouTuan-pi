import qrcode
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

qr = qrcode.QRCode(box_size=1, border=2)
qr.add_data("http://192.168.3.13:666/deposit.html?msg=be69ab95-b5bb-4ccb-8e50-e67b0253a42f+12")
# qr.add_data("http://192.168.3.13:666/deposit.html")
qr.make()
im = qr.make_image()

image.paste(im, (0, 0))

disp.image(image)
disp.display()
