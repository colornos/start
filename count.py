import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(18)
    if input_state == False:
        print('Button Pressed')
        time.sleep(0.5)

	f1=open("one.txt", "w")
	f1.write("0")
	f1.close()

        f2=open("two.txt", "w")
        f2.write("0")
	f2.close()

        f3=open("three.txt", "w")
        f3.write("0")
	f3.close()

        f4=open("four.txt", "w")
        f4.write("0")
	f4.close()

        #Configure LED Output Pin
        LED = 16
        GPIO.setup(LED, GPIO.OUT)
        GPIO.output(LED, GPIO.LOW)

        GPIO.output(LED, GPIO.HIGH)  #Turn on LED
        time.sleep(5)                #Wait 5 Seconds
        GPIO.output(LED, GPIO.LOW)   #Turn off LED

        print "NFC reset"
