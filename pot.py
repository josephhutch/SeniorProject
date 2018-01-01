from __future__ import division
import spidev
import time
import os

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

conn = spidev.SpiDev(0, 0)
conn.max_speed_hz = 1200000 # 1.2 MHz

while 1:
	os.system("amixer -c 1 sset 'Headphone' %s%%" % int(read()*100))
	time.sleep(0.2)
		

