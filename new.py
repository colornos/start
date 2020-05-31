from gpiozero import RGBLED, Button
from time import sleep

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
        led.color = (0,0,0)
    elif count == 2:
	led.color = (0,0.5,0)
        with open('run.sh', 'r') as file:
            data = file.readlines()
        data[7] = "sudo python MBP70.py" + '\n'
        with open('run.sh', 'w') as file:
            file.writelines(data)
        sleep(1)
        led.color = (0,0,0)
    elif count == 3:
	led.color = (0.5,0,0)
        with open('run.sh', 'r') as file:
            data = file.readlines()
        data[7] = "sudo python BW300.py" + '\n'
        with open('run.sh', 'w') as file:
            file.writelines(data)
        sleep(1)
        led.color = (0,0,0)
    elif count == 4:
	led.color = (0.5,0.5,0)
        with open('run.sh', 'r') as file:
            data = file.readlines()
        data[7] = "sudo python Contour7830.py" + '\n'
        with open('run.sh', 'w') as file:
            file.writelines(data)
        sleep(1)
        led.color = (0,0,0)
    elif count == 5:
        led.color = (0.5,0.5,0.5)
        sleep(1)
        led.color = (0,0,0)
        count = 0
    print(count)
