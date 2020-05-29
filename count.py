import RPi.GPIO as GPIO
from time import sleep


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(16,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(18,GPIO.IN, pull_up_down=GPIO.PUD_UP)

count = 0

while True:
    while GPIO.input(18) == 1:
        sleep(0.2)
      
    count = count + 1
    GPIO.output(16,GPIO.HIGH)
    
    while GPIO.input(18) == 0:
        sleep(0.2)   
         
    GPIO.output(16,GPIO.LOW)
    print(count)
    
    if count == 2:
        GPIO.output(26,GPIO.HIGH)
        sleep(1)
        GPIO.output(26,GPIO.LOW)
        GPIO.output(5,GPIO.HIGH)
        sleep(1)
        GPIO.output(5,GPIO.LOW)
        
    elif count == 3:
        GPIO.output(26,GPIO.HIGH)
        
    elif count == 4:
        GPIO.output(26,GPIO.LOW)
        GPIO.output(8,GPIO.HIGH)
    elif count == 5:
        count = 0
        GPIO.output(8,GPIO.LOW)
