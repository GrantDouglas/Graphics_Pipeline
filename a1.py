#!/usr/bin/python3

import math, time, sys, array, itertools
import numpy as np
from PIL import Image
from random import shuffle
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


class coords:
    def __init__(self, x, y, z):
        self.xCoord = x
        self.yCoord = y
        self.zCoord = z

    def send_vals(self):
        return (self.xCoord, self.yCoord, self.zCoord)

    def set_x(self, val):
        self.xCoord = val

    def set_y(self, val):
        self.yCoord = val

    def set_z(self, val):
        self.zCoord = val

    def get_x(self):
        return self.xCoord

    def get_y(self):
        return self.yCoord

    def get_z(self):
        return self.zCoord


def xTransform(points, angle):
    for i in points:
        y = i.get_y()
        z = i.get_z()

        newy = int(y * math.cos(angle) - z * math.sin(angle))
        newz = int(y * math.sin(angle) + z * math.cos(angle))

        i.set_y(newy)
        i.set_z(newz)


def yTransform(points, angle):
    for i in points:
        x = i.get_x()
        z = i.get_z()

        newx = int(x * math.cos(angle) + z * math.sin(angle))
        newz = int(z * math.cos(angle) - x * math.sin(angle))

        i.set_x(newx)
        i.set_z(newz)


def zTransform(points, angle):
    for i in points:
        x = i[0]
        y = i[1]

        newx = int(x * math.cos(angle) + y * math.sin(angle))
        newy = int(y * math.cos(angle) - x * math.sin(angle))

        i[0] = newx
        i[1] = newy


def rasterize(point1, point2, image):
    dx = abs(point2.get_x() - point1.get_x())
    dy = abs(point2.get_y() - point1.get_y())

    if dx > dy:
        length = dx
    elif dy > dx:
        length = dy
    else:
        length = 1

    dx = (point2.get_x() - point1.get_x())/float(length)
    dy = (point2.get_y() - point1.get_y())/float(length)

    x = point1.get_x()
    y = point1.get_y()
    image[math.ceil(x)][math.ceil(y)].cRed = 255
    image[math.ceil(x)][math.ceil(y)].cGreen = 255
    image[math.ceil(x)][math.ceil(y)].cBlue = 255

    for i in range(length-1):
        x += dx
        y += dy
        image[math.ceil(x)][math.ceil(y)].cRed = 255
        image[math.ceil(x)][math.ceil(y)].cGreen = 255
        image[math.ceil(x)][math.ceil(y)].cBlue = 255


def connect(matrix, resolution, key):
    connectionPoints = []

    for x in matrix:
        if (x.send_vals()[0] - key.send_vals()[0] == 0 and x.send_vals()[2] == key.send_vals()[2])\
        or (x.send_vals()[1] - key.send_vals()[1] == 0 and x.send_vals()[2] == key.send_vals()[2])\
        or (x.send_vals()[2] - key.send_vals()[2] != 0 and x.send_vals()[1] == key.send_vals()[1] and x.send_vals()[0] == key.send_vals()[0]):
            connectionPoints.append(x)

    for x in matrix:
        if (x.get_x() == key.get_y() and x.get_y() == key.get_x() and x.get_z() == key.get_z())\
        or (x.get_z() == key.get_x() and x.get_x() == key.get_z() and x.get_y() == key.get_y())\
        or (x.get_y() == key.get_z() and x.get_z() == key.get_y() and x.get_x() == key.get_x()):

            connectionPoints.append(x)

    return connectionPoints

def circleCoords(startX, startY, radius):
    x = radius - 1
    y = 0

    dx = 1
    dy = 1

    error = dx - (radius << 1)

    points = []

    while x >= y:
        points.append([startX + x, startY + y, -128])
        points.append([startX + y, startY + x, -128])
        points.append([startX - y, startY + x, -128])
        points.append([startX - x, startY + y, -128])
        points.append([startX - x, startY - y, -128])
        points.append([startX - y, startY - x, -128])
        points.append([startX + y, startY - x, -128])
        points.append([startX + x, startY - y, -128])

        if error <= 0:
            y += 1
            error += dy
            dy += 2
        else:
            x -= 1
            dx += 2
            error += dx - (radius << 1)

    return points


def sphere(resolution, mesh):
    points = circleCoords(128, 0, 128)
    finalPoints = []
    for x in points:
        if x not in finalPoints:
            finalPoints.append(x)

    coordList = [coords(x[0], x[1], x[2]) for x in finalPoints]

    for k in coordList:
        k.set_x(k.xCoord+300)
        k.set_y(k.yCoord+300)
        k.set_z(k.zCoord+300)

    print(points)

    image = [[RGB(0, 0, 0) for x in range(800)] for y in range(800)]

    # place a value of 255 on the image where the cube will be
    for i in coordList:
        image[i.get_x()][i.get_y()].cRed = 255
        image[i.get_x()][i.get_y()].cGreen = 255
        image[i.get_x()][i.get_y()].cBlue = 255

    # rasterize a line between the key and each of its respective points

    newImage = image

    for m, i in enumerate(image):
        for n, j in enumerate(i):
            newImage[m][n] = (j.cRed, j.cGreen, j.cBlue)

    arr = np.array(image, dtype=np.uint8)

    # print(arr)

    img = Image.fromarray(arr, 'RGB')
    img.save('testing.png')


def cube(res, mesh):
    points = [
        [128, 128, -128],
        [-128, 128, -128],
        [128, -128, -128],
        [-128, -128, -128],
        [128, 128, 128],
        [-128, 128, 128],
        [128, -128, 128],
        [-128, -128, 128]
        ]

    if mesh == "triag":
        triangGrid = triangleMesh(res, points)
        newPoints = triangGrid + points
    elif mesh == "poly":
        newPoints = points
    else:
        print("not valid mesh")
        sys.exit(1)

    finalPoints = []
    matrix = []
    connections = {}

    for x in newPoints:
        if x not in finalPoints:
            finalPoints.append(x)

    coordList = [coords(x[0], x[1], x[2]) for x in finalPoints]

    connect(coordList, resolution, coordList[0])

    for k in coordList:
        k.set_x(k.xCoord)
        k.set_y(k.yCoord)
        k.set_z(k.zCoord)
        matrix.append(k)

    for x in matrix:
        print(x.send_vals())

    coordSet = [x for x in matrix]

    for key in coordSet:
        connections[key] = connect(coordList, resolution, key)

    # transform the x and y coordinates to make 3d shape more clear
    yTransform(matrix, angle)
    xTransform(matrix, angle)

    for k in coordList:
        k.set_x(k.xCoord+300)
        k.set_y(k.yCoord+300)
        k.set_z(k.zCoord+300)

    return connections, matrix


def triangleMesh(resolution, points):
    new = list(itertools.combinations(points, 2))
    final = []

    for x in new:
        if (x[1][0] - x[0][0] == 0 and x[1][2] == x[0][2]) or (x[1][1] - x[0][1] == 0 and x[1][2] == x[0][2]) or (x[1][2] - x[0][2] != 0 and x[1][1] == x[0][1] and x[1][0] == x[0][0]):
            final.append(x)

    newFinal = []

    for x in final:
        if x[1][2] - x[0][2] != 0:
            gap = int((abs(x[0][2]) + abs(x[1][2])) / resolution)
            start = min(x[0][2], x[1][2])
            end = max(x[0][2], x[1][2])

            for k in range(start, end, gap):
                newFinal.append([x[0][0], x[0][1], k])

        elif x[1][0] - x[0][0] == 0:
            gap = int((abs(x[0][1]) + abs(x[1][1])) / resolution)
            start = min(x[0][1], x[1][1])
            end = max(x[0][1], x[1][1])

            for k in range(start, end, gap):
                newFinal.append([x[0][0], k, x[0][2]])

        elif x[1][1] - x[0][1] == 0:
            gap = int((abs(x[0][0]) + abs(x[1][0])) / resolution)
            start = min(x[0][0], x[1][0])
            end = max(x[0][0], x[1][0])

            for k in range(start, end, gap):
                newFinal.append([k, x[0][1], x[0][2]])

    return newFinal

if __name__ == "__main__":
    np.set_printoptions(threshold=np.nan)

    if len(sys.argv) != 5:
        print("not enough arguments")
        sys.exit(1)

    angle = float(sys.argv[1])
    shape = sys.argv[2]
    mesh = sys.argv[3]
    resolution = int(sys.argv[4])

    if shape == "cube":
        connections, matrix = cube(resolution, mesh)
    elif shape == "sphere":
        connections, matrix = sphere(resolution, mesh)
    else:
        print("WIP")
        sys.exit(1)

    # create an image matrix that is empty
    image = [[RGB(0, 0, 0) for x in range(800)] for y in range(800)]

    # place a value of 255 on the image where the cube will be
    for i in matrix:
        image[i.get_x()][i.get_y()].cRed = 255
        image[i.get_x()][i.get_y()].cGreen = 255
        image[i.get_x()][i.get_y()].cBlue = 255

    # rasterize a line between the key and each of its respective points
    for key, val in connections.items():
        for point in val:
            rasterize(key, point, image)

    newImage = image

    for m, i in enumerate(image):
        for n, j in enumerate(i):
            newImage[m][n] = (j.cRed, j.cGreen, j.cBlue)

    arr = np.array(image, dtype=np.uint8)

    # print(arr)

    img = Image.fromarray(arr, 'RGB')
    img.save('testing.png')
