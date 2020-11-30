#!/usr/bin/env python3

# written 2020-10-15 by mza
# based on https://github.com/mzandrew/eink-clock/blob/master/clock.py
# last updated 2020-11-30 by mza

import make_clock
import PythonMagick # sudo apt install -y imagemagick python3-pythonmagick
from PIL import Image as PILImage # sudo apt install -y python3-willow
width = 64
height = 64
resolution = PythonMagick.Geometry(width, height)
import time
import datetime
# from https://stackoverflow.com/a/6209894/5728815
import inspect
import os
import sys
#filename = inspect.getframeinfo(inspect.currentframe()).filename
#path = os.path.dirname(os.path.abspath(filename)) + "/timecache"
#path = "/tmp/timecache"
path = "/opt/timecache"
#print("using " + path)
if not os.path.isdir(path):
	os.mkdir(path)
import stat
#if not os.access(path, os.W_OK):
#	os.chmod(path, stat.S_IRWXU | stat.S_IRWXG)
os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH)
fake_it = False
if not fake_it:
	import rgbmatrix
	options = rgbmatrix.RGBMatrixOptions()
	options.rows = 64
	options.cols = 64
	options.hardware_mapping = "adafruit-hat-pwm"
	matrix = rgbmatrix.RGBMatrix(options = options)
	make_clock.set_width(width)
	make_clock.set_height(height)

def setup(time=datetime.datetime.now()):
	hhmm = "%02d%02d" % (time.hour, time.minute)
	#print(hhmm)
	svgfile = path + "/" + hhmm + ".svg"
	pngfile = path + "/" + hhmm + ".png"
	if not os.path.isfile(pngfile):
		if not os.path.isfile(svgfile):
			#print("")
			#print(str(datetime.datetime.now()) + " setup(" + str(time) + ")")
			make_clock.generate_clock(svgfile, time) # generates an svg file with a clockface of the given time
			#print(str(datetime.datetime.now()) + " setup() midway 1")
			image = PythonMagick.Image(svgfile)
			#print(str(datetime.datetime.now()) + " setup() midway 2")
			image.resize(resolution)
			#print(str(datetime.datetime.now()) + " setup() midway 3")
			image.write(pngfile)
			#print(str(datetime.datetime.now()) + " setup() midway 4")
		global img
		img = PILImage.open(pngfile)
		img = img.convert('RGB')
		#print(str(datetime.datetime.now()) + " setup() complete")

def show():
	#print(str(datetime.datetime.now()) + " show()")
	if not fake_it:
		matrix.SetImage(img)
	#print(str(datetime.datetime.now()) + " show() complete")

def once():
	setup()
	show()

def run():
	while True:
		setup(datetime.datetime.now() + datetime.timedelta(minutes=1))
		sleeptime = 60 - datetime.datetime.utcnow().second
		#print("wait(" + str(sleeptime) + ")")
		time.sleep(sleeptime)
		show()

once()
run()

