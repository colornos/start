import RPi.GPIO as GPIO
import MFRC522
import signal
import time
from time import sleep

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
#print "Welcome to the MFRC522 data read example"
#print "Press Ctrl-C to stop."

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    #if status == MIFAREReader.MI_OK:
        #print "Card detected"
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

	one = uid[0]
	two = uid[1]
	three = uid[2]
	four = uid[3]

	f1=open("one.txt", "w")
	f1.write(str(one))
	f1.close()

        f2=open("two.txt", "w")
        f2.write(str(two))
	f2.close()

        f3=open("three.txt", "w")
        f3.write(str(three))
	f3.close()

        f4=open("four.txt", "w")
        f4.write(str(four))
	f4.close()

	print "Card read UID: %s,%s,%s,%s" % (one, two, three, four)

        #Configure LED Output Pin
        LED = 29
        GPIO.setup(LED, GPIO.OUT)

        GPIO.output(LED, GPIO.HIGH)
        sleep(2)
        GPIO.output(LED, GPIO.LOW)

##        # Authenticate
##        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

##        # Check if authenticated
##        if status == MIFAREReader.MI_OK:
##            MIFAREReader.MFRC522_Read(8)
##            MIFAREReader.MFRC522_StopCrypto1()
##        else:
##            print "Authentication error"
