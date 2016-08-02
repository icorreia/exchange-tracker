#! /usr/bin/python
# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
import json
import time
import pyglet
import matplotlib.pyplot as plt
from Queue import Queue
###########################################################

lb_limit = 0.0
ub_limit = 0.0

time_axis = Queue()
value_axis = Queue()
time_xticks = Queue()

alarm = pyglet.media.load('MGS-theme.ogg')

while True:
	p = Popen(['curl', 'https://api-fxtrade.oanda.com/v1/candles?instrument=EUR_GBP&count=1'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output, err = p.communicate(b"input data that is passed to subprocess' stdin")

	contents = json.loads(output)
	gbp_val = contents["candles"][0]["closeBid"]
	eur_val = 1.0 / float(contents["candles"][0]["closeAsk"])
	
	current_lb = float(str(eur_val)[:5])
	current_ub = float(str(eur_val)[:5]) + 0.001
	
	if (lb_limit != current_lb):
		tendency = "^^^ UP ^^^"
		if (lb_limit > current_lb):
			tendency = "vvv DOWN vvv"
		lb_limit = current_lb
		ub_limit = current_ub
		print "%s %s - %s : %f€" % (tendency, lb_limit, ub_limit, eur_val)		
	else:
		print eur_val

	# ALARMS
	if (eur_val < 1.1900):
		alarm.play()
		print "ALARM: Exchange value is under the limit!"
		# The song lasts for 3:52.
		time.sleep(235)
		alarm.stop()
		alarm.clear()
	time.sleep(6)
