#!/usr/bin/python3

import math, time, sys, array
import numpy as np 
from PIL import Image
# import fbpy as fb


class RGB:
	def __init__(self, red, green, blue):
		self.cRed = red
		self.cBlue = blue
		self.cGreen = green



def xTransform(points, angle):
	for i in points:
		y = i[1]
		z = i[2]

		newy = int(y * math.cos(3.14/4) - z * math.sin(3.14/4))
		newz = int(y * math.sin(3.14/4) + z * math.cos(3.14/4))

		i[1] = newy
		i[2] = newz

def yTransform(points, angle):
	for i in points:
		x = i[0]
		z = i[2]

		newx = int(x * math.cos(angle) + z * math.sin(angle))
		newz = int(z * math.cos(angle) - x * math.sin(angle))

		i[0] = newx
		i[2] = newz

def rasterize(point1, point2, image):
	dx = abs(point2[0] - point1[0])
	dy = abs(point2[1] - point1[1])

	if dx >= dy:
		length = dx
	else:
		length = dy

	dx = (point2[0] - point1[0])/float(length)
	dy = (point2[1] - point1[1])/float(length)

	x = point1[0]
	y = point1[1]
	image[math.ceil(x)][math.ceil(y)] = 255


	for i in range(length-1):
		x += dx
		y += dy
		image[math.ceil(x)][math.ceil(y)] = 255

def oneDimension(x, y):
	return y * 800 + x

np.set_printoptions(threshold=np.nan)

angle = float(sys.argv[1])

w, h = 255, 255;

points = [
		[128,128,-128],
		[-128,128,-128],
		[128,-128,-128],
		[-128,-128,-128],
		[128,128,128],
		[-128,128,128],
		[128,-128,128],
		[-128,-128,128]
		]

angle = 3.1415/4

# print(points)

yTransform(points, angle)
xTransform(points, angle)

# print(points) y * 800 + x

matrix = []
count = 0

# add 300 to each point so its actually on the screen
for k in points:
	k[0] += 300
	k[1] += 300
	matrix.append(k[:2])

image = [[0 for x in range(800)] for y in range(800)]



# place a value of 255 on the image where the cube will be
for i in matrix:
	image[i[0]][i[1]] = 255
	

finalMatrix = [tuple(l) for l in matrix]

# make a hashmap relating each point to its respective connections
connections = {
				finalMatrix[0]: [finalMatrix[1], finalMatrix[2], finalMatrix[4]],
				finalMatrix[1]: [finalMatrix[3], finalMatrix[5], finalMatrix[0]],
				finalMatrix[2]: [finalMatrix[0], finalMatrix[3], finalMatrix[6]],
				finalMatrix[3]: [finalMatrix[1], finalMatrix[2], finalMatrix[7]],
				finalMatrix[4]: [finalMatrix[5], finalMatrix[0], finalMatrix[6]],
				finalMatrix[5]: [finalMatrix[1], finalMatrix[4], finalMatrix[7]],
				finalMatrix[6]: [finalMatrix[2], finalMatrix[7], finalMatrix[4]],
				finalMatrix[7]: [finalMatrix[5], finalMatrix[3], finalMatrix[6]],
}

for key, val in connections.items():
	for point in val:
		rasterize(key, point, image)
	print(val)

print(image)

string = ''.join(str(e) for e in image)


print(connections)

arr = np.array(image)


print(arr)



