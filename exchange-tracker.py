#! /usr/bin/python
# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
import json
import time
import pyglet
###########################################################

lb_limit = 0.0
ub_limit = 0.0

ALARM_LIMIT = 1.183         # The value considered low enough to bet on GBP
HAS_REACHED_MIN = False     # To monitor if we have crossed the lower limit for the currency
min_val = 10000             # The minimum value of GBP during the whole execution period

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
	if (eur_val < min_val):
		min_val = eur_val
		print "Reached new minimum: %f€" % min_val

	if (eur_val < ALARM_LIMIT):
		HAS_REACHED_MIN = True

	# If we have crossed the lower limit and the value seems to be growing.
	if (HAS_REACHED_MIN and eur_val >= min_val + 0.0004):
		alarm = pyglet.media.load('MGS-theme.ogg')
                alarm.play()
                print "ALARM: Exchange value is under the limit (%f€)!" % eur_val
                # The song lasts for 3:52.
                time.sleep(230)


	time.sleep(6)
