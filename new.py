import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT)

for count in range(0, 6):
    GPIO.output(29, GPIO.HIGH)
    sleep(0.1)
    GPIO.output(29, GPIO.LOW)
    sleep(0.1)
