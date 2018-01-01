#! /usr/bin/python
from __future__ import division
import thread
import os
import time
import Adafruit_Trellis
import spidev
import RPi.GPIO as GPIO

MOMENTARY = 0
LATCHING = 1
MODE = LATCHING


def playSound(sound):
	os.system("aplay -N %s &" % str(sound))


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
b3 = [0] * 128
b4 = [0] * 128
b5 = [0] * 128
b6 = [0] * 128
b7 = [0] * 128
b8 = [0] * 128
b9 = [0] * 128
b10 = [0] * 128
b11 = [0] * 128
b12 = [0] * 128
b13 = [0] * 128
b14 = [0] * 128
b15 = [0] * 128
b16 = [0] * 128


print 'Milestone 3 Demo'

trellis.begin((0x70, I2C_BUS))   # only one

def readPad():
	if trellis.readSwitches():
		# go through every button
		for i in range(numKeys):
			# if it was pressed...
			if trellis.justPressed(i):
				if i==0:
					b1[cnt%128] = 1
				if i==1:
					b2[cnt%128] = 1
				if i==2:
					b3[cnt%128] = 1
				if i==3:
					b4[cnt%128] = 1
				if i==4:
					b5[cnt%128] = 1
				if i==5:
					b6[cnt%128] = 1
				if i==6:
					b7[cnt%128] = 1
				if i==7:
					b8[cnt%128] = 1
				if i==8:
					b9[cnt%128] = 1
				if i==9:
					b10[cnt%128] = 1
				if i==10:
					b11[cnt%128] = 1
				if i==11:
					b12[cnt%128] = 1
				if i==12:
					b13[cnt%128] = 1
				if i==13:
					b14[cnt%128] = 1
				if i==14:
					b15[cnt%128] = 1
				if i==15:
					b16[cnt%128] = 1

def adjustVolume():
	os.system("amixer -q -c 1 sset 'Headphone' %s%%" % int(read()*100))
	
def bitstring(n):
	s = bin(n)[2:]
	return '0'*(8-len(s)) + s

def read(adc_channel=0, spi_channel=0):
	cmd = 128
	if adc_channel:
		cmd += 32
	reply_bytes = conn.xfer2([cmd, 0])
	reply_bitstring = ''.join(bitstring(n) for n in reply_bytes)
	reply = reply_bitstring[5:15]
	return int(reply, 2) / 2**10


pressed5last = False  #metronome on/off
pressed6last = False  #start/stop
pressed13last = False #tempo-up
pressed26last = False #tempo-down
metronome = True
stopped = False
def readButtons():
	global pressed5last
	global pressed6last
	global pressed13last
	global pressed26last
	global metronome
	global bpm
	global stopped
	global b1
	global b2
	global b3
	global b4
	global b5
	global b6
	global b7
	global b8
	global b9
	global b10
	global b11
	global b12
	global b13
	global b14
	global b15
	global b16

	while 1:
		is5Pressed = GPIO.input(5)
		is6Pressed = GPIO.input(6)
		is13Pressed = GPIO.input(13)
		is26Pressed = GPIO.input(26)

		if is5Pressed == True and pressed5last == False:
			pressed5last = True
		elif is5Pressed == False and pressed5last == True:
			pressed5last = False
			metronome = not metronome
		if is6Pressed == True and pressed6last == False:
			pressed6last = True
		elif is6Pressed == False and pressed6last == True:
			pressed6last = False
			stopped = not stopped
			b1 = [0] * 128
			b2 = [0] * 128
			b3 = [0] * 128
			b4 = [0] * 128
			b5 = [0] * 128
			b6 = [0] * 128
			b7 = [0] * 128
			b8 = [0] * 128
			b9 = [0] * 128
			b10 = [0] * 128
			b11 = [0] * 128
			b12 = [0] * 128
			b13 = [0] * 128
			b14 = [0] * 128
			b15 = [0] * 128
			b16 = [0] * 128

		if is13Pressed == True and pressed13last == False:
			pressed13last = True
		elif is13Pressed == False and pressed13last == True:
			pressed13last = False
			bpm +=1
		if is26Pressed == True and pressed26last == False:
			pressed26last = True
		elif is26Pressed == False and pressed26last == True:
			pressed26last = False
			bpm -=1

		time.sleep(0.005)



conn = spidev.SpiDev(0, 0)
conn.max_speed_hz = 1200000 # 1.2 MHz

GPIO.setmode(GPIO.BCM)
GPIO.setup([5, 6, 13, 26], GPIO.IN)

thread.start_new_thread(readButtons, ())

while True:
	thread.start_new_thread(adjustVolume, ())
	if not stopped:
		thread.start_new_thread(readPad, ())

		if cnt%16 == 0 and metronome == True:
			thread.start_new_thread(playSound, ('~/seniorproj/examples/tick.wav',))
		if b1[cnt%128] == 1:
			thread.start_new_thread(playSound, ('~/seniorproj/examples/audio1.wav',))
		if b2[cnt%128] == 1:
			thread.start_new_thread(playSound, ('~/seniorproj/examples/audio2.wav',))
		if b3[cnt%128] == 1:
			thread.start_new_thread(playSound, ('~/seniorproj/examples/audio3.wav',))
		if b4[cnt%128] == 1:
			thread.start_new_thread(playSound, ('~/seniorproj/examples/audio4.wav',))
		if b5[cnt%128] == 1:
			thread.start_new_thread(playSound, ('~/seniorproj/examples/audio5.wav',))
		if b6[cnt%128] == 1:
			thread.start_new_thread(playSound, ('~/seniorproj/examples/audio6.wav',))
		if b7[cnt%128] == 1:
			thread.start_new_thread(playSound, ('~/seniorproj/examples/audio7.wav',))
		if b8[cnt%128] == 1:
			thread.start_new_thread(playSound, ('~/seniorproj/examples/audio8.wav',))
		if b9[cnt%128] == 1:
			thread.start_new_thread(playSound, ('~/seniorproj/examples/audio9.wav',))
		if b10[cnt%128] == 1:
			thread.start_new_thread(playSound, ('~/seniorproj/examples/audio10.wav',))
		if b11[cnt%128] == 1:
			thread.start_new_thread(playSound, ('~/seniorproj/examples/audio11.wav',))
		if b12[cnt%128] == 1:
			thread.start_new_thread(playSound, ('~/seniorproj/examples/audio12.wav',))
		if b13[cnt%128] == 1:
			thread.start_new_thread(playSound, ('~/seniorproj/examples/audio13.wav',))
		if b14[cnt%128] == 1:
			thread.start_new_thread(playSound, ('~/seniorproj/examples/audio14.wav',))
		if b15[cnt%128] == 1:
			thread.start_new_thread(playSound, ('~/seniorproj/examples/audio15.wav',))
		if b16[cnt%128] == 1:
			thread.start_new_thread(playSound, ('~/seniorproj/examples/audio16.wav',))
		
		cnt = cnt + 1

	divisions = 60.0/bpm/16

	time.sleep(divisions)
