from gpiozero import Servo, Button
from time import sleep

btn = Button(10)
btn.wait_for_active()
print("active")
# while True:
#     print(btn.is_active)
#     sleep(0.2)
