import requests
import json

import qrcode
import time

import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from gpiozero import Servo, Button

with open("config.json") as f:
    cfg = json.loads(f.read())

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
font = ImageFont.truetype("SourceHanSans-Regular.ttc", 16)

state = [False for i in range(cfg["cabinet_num"])]
servos = [Servo(pin, min_pulse_width=0.03*20/1000,
                max_pulse_width=0.12*20/1000,
                initial_value=None) for pin in cfg["servo_pin"]]
btns = [Button(pin) for pin in cfg["btn_pin"]]

HOST = cfg["host"]


def disp_qrcode():
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    qr = qrcode.QRCode(box_size=1, border=2)

    idx = 0
    while idx < cfg["cabinet_num"] and state[idx]:
        idx += 1

    if idx == cfg["cabinet_num"]:
        qr.add_data(f"{HOST}/full.html")
    else:
        qr.add_data(f"{HOST}/deposit.html?d={cfg['device_id']}&c={idx}")
    qr.make()
    im = qr.make_image()
    image.paste(im, (0, 0))
    draw.text(
        (0, 40),
        f"剩余空柜数：{cfg['cabinet_num'] - idx}",
        font=font, fill=255
    )

    disp.image(image)
    disp.display()


def disp_waiting():
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), "等待柜门关闭...", font=font, fill=255)
    disp.image(image)
    disp.display()


def open_cabinet(no):
    print("open_cabinet", no)
    servos[no].max()
    time.sleep(1)
    servos[no].detach()


def close_cabinet(no):
    print("close_cabinet", no)
    servos[no].min()
    time.sleep(1)
    servos[no].detach()


def api(path):
    return f"{HOST}/api{path}"


ss = requests.Session()
r = ss.post(api("/login/check"))
print(r.text)
r = ss.post(
    api("/login"),
    {"username": cfg["device_id"], "passwd": cfg["passwd"]}
)
print(r.text)
r = ss.post(api("/login/check"))
print(r.text)


def update():
    try:
        r = ss.get(api("/open/list"))
    except:
        print("network error")
    print(r.text, state)
    obj = json.loads(r.text)
    for d in obj["data"]:
        no = d["cabinet_no"]
        state[no] = d["state"] == 0
        disp_waiting()
        open_cabinet(no)
        time.sleep(0.5)
        btns[no].wait_for_active()
        close_cabinet(no)


while True:
    update()
    disp_qrcode()
    time.sleep(1)
