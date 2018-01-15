#!/usr/bin/python3

from PIL import Image
import math

def xTransform(points):
	for i in points:
		y = i[1]
		z = i[2]
		
		newy = int(y * math.cos(3.14/4) - z * math.sin(3.14/4))
		newz = int(y * math.sin(3.14/4) + z * math.cos(3.14/4))

		i[1] = newy
		i[2] = newz

def yTransform(points):
	for i in points:
		x = i[0]
		z = i[2]

		newx = int(x * math.cos(3.14/4) + z * math.sin(3.14/4))
		newz = int(z * math.cos(3.14/4) - x * math.sin(3.14/4))

		i[0] = newx
		i[2] = newz


w, h = 255, 255;
Matrix = [[0 for x in range(w)] for y in range(h)]


points = [
		[128,128,-128],
		[-128,128,-128],
		[128,-128,-128],
		[-128,-128,-128],
		[128,128,-128],
		[-128,128,128],
		[128,-128,128],
		[-128,-128,128]
		]

# print(points)

yTransform(points)
xTransform(points)

print(points)


print("hello")

# im = Image.open("test.jpg")
# im.show()