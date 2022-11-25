from gpiozero import Servo, Button
from time import sleep


servo = Servo(17, min_pulse_width=0.03*20/1000, max_pulse_width=0.12*20/1000)

while True:
    servo.min()
    sleep(1)
    servo.mid()
    sleep(1)
    servo.max()
    sleep(1)
