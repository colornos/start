import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

blue = LED(16)
red = LED(27)
green = LED(22)
count = 0

while True:
    input_state = GPIO.input(18)
    if input_state == False:
	count = count + 1
        print('Button Pressed')
        time.sleep(2.5)

        #Configure LED Output Pin
        LED = 16
        GPIO.setup(LED, GPIO.OUT)
        GPIO.output(LED, GPIO.LOW)

        GPIO.output(LED, GPIO.HIGH)  #Turn on LED
        time.sleep(2)                #Wait 5 Seconds
        GPIO.output(LED, GPIO.LOW)   #Turn off LED
	if count = 2:
		print "pressed twice"
	if count = 3:
		print "pressed three times"
	if count = 4:
		print "pressed four times"
	
