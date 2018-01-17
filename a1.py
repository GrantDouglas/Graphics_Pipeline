#!/usr/bin/python3

from PIL import Image, ImageDraw
import math, time, sys
# import fbpy as fb

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

def rasterize(matrix):
	j = 0
	for k in matrix:
		j = 1



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

# angle = 3.1415/4

# print(points)

yTransform(points, angle)
xTransform(points, angle)

# print(points)

matrix = []
count = 0

for k in points:
	k[0] += 300
	k[1] += 300
	matrix.append(k[:2])

finalMatrix = [tuple(l) for l in matrix]

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
	print(val)


print(finalMatrix)

# print(matrix)
# print("hello")

img = Image.new('RGB', (800,800), (0, 0, 0))
draw = ImageDraw.Draw(img)

for key, val in connections.items():
	for x in val:
		draw.line([key,x])

# draw.line(finalMatrix)

# draw.polygon(finalMatrix)
img.save("image.png", "PNG")

img.show()
# im = Image.open("test.jpg")
# im.show()