#!/usr/bin/env python3

# written 2020-10-15 by mza
# based on https://github.com/mzandrew/eink-clock/blob/master/clock.py
# last updated 2020-10-15 by mza

import make_clock
import PythonMagick # sudo apt install -y python3-pythonmagick
from PIL import Image, ImageFont, ImageDraw
width = 64
height = 64
resolution = PythonMagick.Geometry(width, height)
import time
import datetime
# from https://stackoverflow.com/a/6209894/5728815
import inspect
import os
filename = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(filename))
#print(path)
import rgbmatrix
options = rgbmatrix.RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.hardware_mapping = "adafruit-hat-pwm"
matrix = rgbmatrix.RGBMatrix(options = options)

def setup(time=datetime.datetime.now()):
	#print("setup()")
	make_clock.set_width(width)
	make_clock.set_height(height)
	make_clock.generate_clock(path + "/time.svg", time) # generates an svg file with a clockface of the given time
	image = PythonMagick.Image(path + "/time.svg")
	image.resize(resolution)
	image.write(path + "/time.png")

def show():
	#print("show()")
	img = Image.open(path + "/time.png")
	img = img.convert('RGB')
	matrix.SetImage(img)

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

