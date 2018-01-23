#!/usr/bin/python3

import math, time, sys, array, itertools
import numpy as np 
from PIL import Image
# import fbpy as fb


class RGB:
	def __init__(self, red, green, blue):
		self.cRed = red
		self.cBlue = blue
		self.cGreen = green

	def printing(self):
		print(self.cRed)
		print(self.cBlue)
		print(self.cGreen)

def xTransform(points, angle):
	for i in points:
		y = i[1]
		z = i[2]

		newy = int(y * math.cos(angle) - z * math.sin(angle))
		newz = int(y * math.sin(angle) + z * math.cos(angle))

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

def zTransform(points, angle):
	for i in points:
		x = i[0]
		y = i[1]

		newx = int(x * math.cos(angle) + y * math.sin(angle))
		newy = int(y * math.cos(angle) - x * math.sin(angle))

		i[0] = newx
		i[1] = newy

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
	image[math.ceil(x)][math.ceil(y)].cRed = 255
	image[math.ceil(x)][math.ceil(y)].cGreen = 255
	image[math.ceil(x)][math.ceil(y)].cBlue = 255

	for i in range(length-1):
		x += dx
		y += dy
		image[math.ceil(x)][math.ceil(y)].cRed = 255
		image[math.ceil(x)][math.ceil(y)].cGreen = 255
		image[math.ceil(x)][math.ceil(y)].cBlue = 255

def cube():
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

	triangleMesh(2, points)

		# transform the x and y coordinates to make 3d shape more clear
	yTransform(points, angle)
	xTransform(points, angle)

	matrix = []

	print(points)

	

	# print(points)

	# add 300 to each point so its actually on the screen
	for k in points:
		k[0] += 300
		k[1] += 300
		matrix.append(k[:2])

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

	return finalMatrix, connections, matrix

def triangleMesh(resolution, points):
	new = list(itertools.combinations(points, 2))
	final = []
	for x in new:
		if (x[1][0] - x[0][0] == 0 and x[1][2] == x[0][2]) or (x[1][1] - x[0][1] == 0 and x[1][2] == x[0][2]) or (x[1][2] - x[0][2] == 0 and x[1][1] == x[0][1] and x[1][0] == x[0][0]):
			final.append(x)
	print(final)


if __name__ == "__main__":
	np.set_printoptions(threshold=np.nan)

	if len(sys.argv) != 4:
		print("not enough arguments")
		sys.exit(1)

	angle = float(sys.argv[1])
	shape = sys.argv[2]
	mesh = sys.argv[3]


	if shape == "cube":
		finalMatrix, connections, matrix = cube()
		
	else:
		print("WIP")
		sys.exit(1)

	# create an image matrix that is empty
	image = [[RGB(0,0,0) for x in range(800)] for y in range(800)]


	# place a value of 255 on the image where the cube will be
	for i in matrix:
		image[i[0]][i[1]].cRed = 255
		image[i[0]][i[1]].cGreen = 255
		image[i[0]][i[1]].cBlue = 255
		
	# rasterize a line between the key and each of its respective points
	for key, val in connections.items():
		for point in val:
			rasterize(key, point, image)

	newImage = image

	for m,i in enumerate(image):
		for n,j in enumerate(i):
			newImage[m][n] = (j.cRed, j.cGreen, j.cBlue)

	arr = np.array(image, dtype=np.uint8)

	# print(arr)

	img = Image.fromarray(arr, 'RGB')
	img.save('testing.png')
