#!/usr/bin/python3

import math, time, sys, array, itertools
import numpy as np
from PIL import Image


#
#   This is a class used to store the RGB values of the image matrix
#
class RGB:
    def __init__(self, red, green, blue):
        self.cRed = red
        self.cBlue = blue
        self.cGreen = green

    def printing(self):
        print(self.cRed)
        print(self.cBlue)
        print(self.cGreen)

#
#  This is a class that stores all of the coordinates for the points.
#
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

#
#   This function is responsible for transforming the given points through the x axis.
#   In: points  A list of points to be transformed
#       angle   An angle in radians to rotate the x axis by
#
def xTransform(points, angle):
    for i in points:
        y = i.get_y()
        z = i.get_z()

        newy = int(y * math.cos(angle) - z * math.sin(angle))
        newz = int(y * math.sin(angle) + z * math.cos(angle))

        i.set_y(newy)
        i.set_z(newz)


def yTransform(points, angle):
    """Transform points in the y axis

    This function will transform a given list of points on the y axis by a given angle

    Arguments:
        points {List} -- A list of points to bhe rotated
        angle {Float} -- An angle in radians to rotate the axis by
    """

    for i in points:
        x = i.get_x()
        z = i.get_z()

        newx = int(x * math.cos(angle) + z * math.sin(angle))
        newz = int(z * math.cos(angle) - x * math.sin(angle))

        i.set_x(newx)
        i.set_z(newz)


def rasterize(point1, point2, image):
    """Rasterize a line between two points

    This function will rasterize a line between two points using the DDA

    Arguments:
        point1 {coord} -- A coord object which specifies the first point to rasterize
        point2 {coord} -- A coord object which specifies the second point to rasterize
        image {List of RGB} -- The image matrix which stores each points RGB value
    """
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


def connect(matrix, key):
    """creates a connection between a point and all neighbouring points

    This function will create a connection between a point and multiple others
    by checking their adjacency and their plane.

    Arguments:
        matrix {list of coords} -- A matrix of objects which are in the vector space
        key {coord} -- A coord object which contains the coordinate information of the key

    Returns:
        List of coords -- A list of coord objects which are mapped to the key
    """
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
    """Creates a circle

    This function will create a circle using the Midpoint Circle Algorithm

    Arguments:
        startX {int} -- The starting x position of the circle
        startY {int} -- The starting y position of the circle
        radius {int} -- The radius of the circle

    Returns:
        List -- A list of coordinates which create a circle
    """
    x = radius - 1
    y = 0

    delta_x = 1
    delta_y = 1

    error = delta_x - (radius * 2)

    points = []
    points.append([128, 0, -128])

    # plot all points until it hits the y axis
    while x >= y:
        points.append([startX + x, startY + y, -128])
        points.append([startX + y, startY + x, -128])
        points.append([startX - y, startY + x, -128])
        points.append([startX - x, startY + y, -128])
        points.append([startX - x, startY - y, -128])
        points.append([startX - y, startY - x, -128])
        points.append([startX + y, startY - x, -128])
        points.append([startX + x, startY - y, -128])

        # move the y coordinate up if it did not go far enough. otherwise move back an x coordinate
        if error <= 0:
            y += 1
            error += delta_y
            delta_y += 2
        else:
            x -= 1
            delta_x += 2
            error += delta_x - (radius * 2)

    return points


def connectCircle(res, key):
    """Divides a circle into even portions

    This function will divide a circle into portions based on the resolution value

    Arguments:
        resolution {int} -- The triangle resolution specified by the user
        key {coord} -- The centre point of the circle

    Returns:
        list of coords -- A list of coord objects which make up the circle division
    """
    r = 128
    angle = 0
    connectList = []

    for i in range(0, res):

        # create an angle between 0 and 2pi that is split evenly by the resolution number
        angle = i * (6.28 / res)

        # calculate new x and y coordinates that meet the angle specified.
        x = int(key.get_x() + r * math.cos(angle)) + 300
        y = int(key.get_y() + r * math.sin(angle)) + 400
        connectList.append(coords(x, y, -128))

    return connectList


def sphere(resolution, mesh):
    """Creates a sphere
    This function will create a sphere

    Arguments:
        resolution {int} -- The number of triangles to create
        mesh {string} -- The type of mesh to create

    Returns:
        List -- A dictionary where each key is a coord object, and it maps to a list of coord objects
        List -- A matrix which contains coord objects for each point of the sphere
    """
    points = circleCoords(128, 0, 128)
    finalPoints = []
    matrix = []
    connections = {}
    for x in points:
        if x not in finalPoints:
            finalPoints.append(x)

    coordList = [coords(x[0], x[1], x[2]) for x in finalPoints]

    for k in coordList:
        k.set_x(k.xCoord)
        k.set_y(k.yCoord)
        k.set_z(k.zCoord)
        matrix.append(k)

    coordSet = [x for x in matrix]

    print(coordSet[0].send_vals())

    connections[coordSet[0]] = connectCircle(resolution, coordSet[0])

    print(connections)

    for k in matrix:
        k.set_x(k.xCoord+300)
        k.set_y(k.yCoord+400)
        k.set_z(k.zCoord+400)

    return connections, matrix


def cube(res, mesh):
    """Create a cube

    This function will create the points which make up a cube

    Arguments:
        res {int} -- The resolution of the faces on the cube
        mesh {string} -- the mesh type of the cube

   Returns:
        List -- A dictionary where each key is a coord object, and it maps to a list of coord objects
        List -- A matrix which contains coord objects for each point of the sphere
    """
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

    if mesh == "tri":
        triangGrid = grid(res, points)
        newPoints = triangGrid + points
    elif mesh == "poly":
        newPoints = points
    else:
        print("not valid mesh")
        sys.exit(1)

    finalPoints = []
    matrix = []
    connections = {}

    # create a list of unique points
    for x in newPoints:
        if x not in finalPoints:
            finalPoints.append(x)

    coordList = [coords(x[0], x[1], x[2]) for x in finalPoints]

    # store the points in a matrix
    for k in coordList:
        k.set_x(k.xCoord)
        k.set_y(k.yCoord)
        k.set_z(k.zCoord)
        matrix.append(k)

    # create a set out of these coordinates to use as keys for the connection dictionary
    coordSet = [x for x in matrix]

    # create a dictionary which maps each point to a list of connected points
    for key in coordSet:
        connections[key] = connect(coordList, key)

    # transform the x and y coordinates to make 3d shape more clear
    yTransform(matrix, angle)
    xTransform(matrix, angle)

    # move the square to the middle of the image for a cleaner look
    for k in coordList:
        k.set_x(k.xCoord+300)
        k.set_y(k.yCoord+400)
        k.set_z(k.zCoord+400)

    return connections, matrix


def grid(resolution, points):
    """Create a grid on a square surface

    This function will create a grid of a specified resolution onto a surface identified by coordinates

    Arguments:
        resolution {int} -- The resolution of the grid
        points {list} -- The list of points that make up the cube

    Returns:
        list -- A list of points which
    """
    new = list(itertools.combinations(points, 2))
    final = []

    # find all unique pair combinations within the point list
    for x in new:
        if (x[1][0] - x[0][0] == 0 and x[1][2] == x[0][2]) or (x[1][1] - x[0][1] == 0 and x[1][2] == x[0][2]) or (x[1][2] - x[0][2] != 0 and x[1][1] == x[0][1] and x[1][0] == x[0][0]):
            final.append(x)

    newFinal = []

    for x in final:

        # place grid points on z axis lines if the z axis are equal
        if x[1][2] - x[0][2] != 0:
            gap = int((abs(x[0][2]) + abs(x[1][2])) / resolution)
            start = min(x[0][2], x[1][2])
            end = max(x[0][2], x[1][2])

            for k in range(start, end, gap):
                newFinal.append([x[0][0], x[0][1], k])

        # place grid points on y axis lines if the x axis are equal
        elif x[1][0] - x[0][0] == 0:
            gap = int((abs(x[0][1]) + abs(x[1][1])) / resolution)
            start = min(x[0][1], x[1][1])
            end = max(x[0][1], x[1][1])

            for k in range(start, end, gap):
                newFinal.append([x[0][0], k, x[0][2]])

        # place grid points on x axis lines if the y axis are equal
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

    # redirect to appropriate algorithm for the shape
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

    # create a new image matrix with just the colour values of the cells
    for m, i in enumerate(image):
        for n, j in enumerate(i):
            newImage[m][n] = (j.cRed, j.cGreen, j.cBlue)

    arr = np.array(newImage, dtype=np.uint8)

    # print(arr)

    img = Image.fromarray(arr, 'RGB')
    img.save('testing.png')
