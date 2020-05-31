from gpiozero import RGBLED, Button
from time import sleep
import os

led = RGBLED(red=26, green=5, blue=16)
button = Button(18)
count = 0

while True:
    button.wait_for_press()
    
    button.wait_for_release()
    
    count = count + 1
    if count == 1:
        led.color = (0,0,0.5)
        with open('run.sh', 'r') as file:
            data = file.readlines()
        data[7] = "sudo python BS440.py" + '\n'
        with open('run.sh', 'w') as file:
            file.writelines(data)
        sleep(1)
        os.system ('sudo python BS440.py')
        led.color = (0,0,0)
    elif count == 2:
	led.color = (0,0.5,0)
        os.system ('pkill -9 -f BS440.py')
        with open('run.sh', 'r') as file:
            data = file.readlines()
        data[7] = "sudo python MBP70.py" + '\n'
        with open('run.sh', 'w') as file:
            file.writelines(data)
        sleep(1)
        os.system ('sudo python MBP70.py')
        led.color = (0,0,0)
    elif count == 3:
	led.color = (0.5,0,0)
        os.system ('pkill -9 -f MBP70.py')
        with open('run.sh', 'r') as file:
            data = file.readlines()
        data[7] = "sudo python BW300.py" + '\n'
        with open('run.sh', 'w') as file:
            file.writelines(data)
        sleep(1)
        os.system ('sudo python BW300.py')
        led.color = (0,0,0)
    elif count == 4:
	led.color = (0.5,0.5,0)
        os.system ('pkill -9 -f BW300.py')
        with open('run.sh', 'r') as file:
            data = file.readlines()
        data[7] = "sudo python Contour7830.py" + '\n'
        with open('run.sh', 'w') as file:
            file.writelines(data)
        sleep(1)
        os.system ('sudo python Contour7830.py')
        led.color = (0,0,0)
    elif count == 5:
        led.color = (0.5,0.5,0.5)
        os.system ('pkill -9 -f Contour7830.py')
        sleep(1)
        led.color = (0,0,0)
        count = 0
    print(count)
