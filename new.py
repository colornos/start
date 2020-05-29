from gpiozero import LED, Button
from signal import pause


blue = LED(17)
red = LED(27)
green = LED(22)
button = Button(2)
count = 0


while True:
    button.wait_for_press()
    blue.on()
    
    button.wait_for_release()
    blue.off()
    
    count = count + 1
    if count == 3:
        red.on()
    elif count == 4:
        red.off()
        green.on()
    elif count == 5:
        count = 0
        green.off()
    print(count)
