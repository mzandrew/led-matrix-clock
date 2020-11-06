#!/usr/bin/env python3

from PIL import Image, ImageFont, ImageDraw

import time
# from https://stackoverflow.com/a/6209894/5728815
import inspect
import os
filename = inspect.getframeinfo(inspect.currentframe()).filename
#path = os.path.dirname(os.path.abspath(filename))
path = "/tmp"
import rgbmatrix
options = rgbmatrix.RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.hardware_mapping = "adafruit-hat-pwm"
matrix = rgbmatrix.RGBMatrix(options = options)

def show():
	#print("show()")
	img = Image.open(path + "/image.png")
	img = img.convert('RGB')
	matrix.SetImage(img)

while True:
	show()
	time.sleep(1)

