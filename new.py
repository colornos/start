from gpiozero import LED, Button
from signal import pause
import time

blue = LED(16)
red = LED(26)
green = LED(5)
white = LED(4)
yellow = LED(17)
button = Button(18)
count = 0

while True:
    button.wait_for_press()
    blue.on()
    
    button.wait_for_release()
    blue.off()
    
    count = count + 1
    if count == 1:
        yellow.on()
        time.sleep(1)
        yellow.off()
    elif count == 2:
        white.on()
        time.sleep(1)
        white.off()
    elif count == 3:
        white.off()
        red.on()
        time.sleep(1)
        red.off()
    elif count == 4:
        red.off()
        green.on()
        time.sleep(1)
        green.off()
    elif count == 5:
        count = 0
        green.off()
    print(count)
