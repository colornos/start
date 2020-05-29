import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN)

count = 0

while True:
    inputValue = GPIO.input(18)
    if (inputValue == True):
	count = count + 1
        print("Button Pressed " + str(count) + " times.")
        time.sleep(.5)
    time.sleep(.5)

        #Configure LED Output Pin
        #LED = 16
        #GPIO.setup(LED, GPIO.OUT)
        #GPIO.output(LED, GPIO.LOW)

        #GPIO.output(LED, GPIO.HIGH)  #Turn on LED
        #time.sleep(2)                #Wait 5 Seconds
        #GPIO.output(LED, GPIO.LOW)   #Turn off LED
