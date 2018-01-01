import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

chan_list = [5, 6, 13, 26]
GPIO.setup(chan_list, GPIO.IN)

while True:
	is5 = GPIO.input(5)
	is6 = GPIO.input(6)
	is13 = GPIO.input(13)
	is26 = GPIO.input(26)
	if is5 == True:
		print("Five Pressed")
		time.sleep(0.2)
	if is6 == True:
		print("Six Pressed")
		time.sleep(0.2)
	if is13 == True:
		print("Thirteen Pressed")
		time.sleep(0.2)
	if is26 == True:
		print("TwentySix Pressed")
		time.sleep(0.2)
