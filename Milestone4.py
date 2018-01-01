import thread
import os
import time
import Adafruit_Trellis
import pygame

MOMENTARY = 0
LATCHING = 1
MODE = LATCHING


def playSound(sound):
	pygame.mixer.music.load("%s" % str(sound))
	pygame.mixer.music.play()

pygame.mixer.init()

matrix0 = Adafruit_Trellis.Adafruit_Trellis()
trellis = Adafruit_Trellis.Adafruit_TrellisSet(matrix0)

NUMTRELLIS = 1
numKeys = NUMTRELLIS * 16
I2C_BUS = 1


cnt=0
bpm = 60
divisions = 60.0/bpm/16
b1 = [0] * 128
b2 = [0] * 128


print 'Milestone 3 Demo'

trellis.begin((0x70, I2C_BUS))   # only one

def readPad():
	if trellis.readSwitches():
		# go through every button
		for i in range(numKeys):
			# if it was pressed...
			if trellis.justPressed(i):
				print 'v{0}'.format(i)
				if i==0:
				#	thread.start_new_thread(playSound, ('Bass.wav',))
					b1[cnt%128] = 1
				if i==1:
				#	thread.start_new_thread(playSound, ('Snare.wav',))
					b2[cnt%128] = 1


while True:

	thread.start_new_thread(readPad, ())

	if cnt%16 == 0:
		thread.start_new_thread(playSound, ('tick.wav',))
	if b1[cnt%128] == 1:
		thread.start_new_thread(playSound, ('Bass.wav',))
	if b2[cnt%128] == 1:
		thread.start_new_thread(playSound, ('Snare.wav',))

	cnt = cnt + 1

	time.sleep(divisions)
