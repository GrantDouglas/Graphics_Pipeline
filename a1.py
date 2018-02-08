#!/usr/bin/python3


import math, time, sys, array, itertools
import numpy as np
from PIL import Image


class RGB:
    """The class of red green blue values of the image

    This class contains all data pertaining to the red green blue values of the image matrix
    """
    def __init__(self, red, green, blue):
        self.cRed = red
        self.cBlue = blue
        self.cGreen = green

    def printing(self):
        print(self.cRed)
        print(self.cBlue)
        print(self.cGreen)


class coords:
    """The class of coordinates

    This class contains all of the data pertainint to the coordinates of a shape
    """
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
    """Transform points in the x axis

    This function will transform a given list of points on the x axis by a given angle

    Arguments:
        points {List} -- A list of points to bhe rotated
        angle {Float} -- An angle in radians to rotate the axis by
    """
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


def zTransform(points, angle):
    """Transform points in the z axis

    This function will transform a given list of points on the z axis by a given angle

    Arguments:
        points {List} -- A list of points to bhe rotated
        angle {Float} -- An angle in radians to rotate the axis by
    """

    for i in points:
        x = i.get_x()
        y = i.get_y()

        newx = int(x * math.cos(angle) - y * math.sin(angle))
        newy = int(y * math.cos(angle) + x * math.sin(angle))

        i.set_x(newx)
        i.set_y(newy)


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


def circleCoords(startX, startY, radius, axis, res, vol):
    """Creates a circle

    This function will create a circle using the Midpoint Circle Algorithm

    Arguments:
        startX {int} -- The starting x position of the circle
        startY {int} -- The starting y position of the circle
        radius {int} -- The radius of the circle

    Returns:
        List -- A list of coordinates which create a circle
    """

    angleList = []

    if axis == 'x':
        x = radius - 1
        y = 0

        delta_x = 1
        delta_y = 1

        error = delta_x - (radius * 2)

        points = []
        points.append([vol, 0, -vol])

        # plot all points until it hits the y axis
        while x >= y:
            points.append([startX + x, startY + y, -vol])
            points.append([startX + y, startY + x, -vol])
            points.append([startX + y, startY - x, -vol])
            points.append([startX + x, startY - y, -vol])
            points.append([startX - y, startY + x, -vol])
            points.append([startX - x, startY + y, -vol])
            points.append([startX - x, startY - y, -vol])
            points.append([startX - y, startY - x, -vol])

            # move the y coordinate up if it did not go far enough. otherwise move back an x coordinate
            if error <= 0:
                y += 1
                error += delta_y
                delta_y += 2
            else:
                x -= 1
                delta_x += 2
                error += delta_x - (radius * 2)
    elif axis == 'z':
        x = radius - 1
        z = 0

        delta_x = 1
        delta_z = 1

        error = delta_x - (radius * 2)

        points = []
        points.append([vol, vol, -vol])
        points.append([vol, 0, -vol])

        # plot all points until it hits the y axis
        while x >= z:
            points.append([startX + x, 0, startY + z])
            points.append([startX + z, 0, startY + x])

            points.append([startX + z, 0, startY - x])
            points.append([startX + x, 0, startY - z])
            points.append([startX - z, 0, startY + x])
            points.append([startX - x, 0, startY + z])
            points.append([startX - x, 0, startY - z])
            points.append([startX - z, 0, startY - x])

            # move the y coordinate up if it did not go far enough. otherwise move back an x coordinate
            if error <= 0:
                z += 1
                error += delta_z
                delta_z += 2
            else:
                x -= 1
                delta_x += 2
                error += delta_x - (radius * 2)

    finalPoints = points
    return finalPoints, angleList


def connectCircle(res, key, axis, points, volume):
    """Divides a circle into even portions

    This function will divide a circle into portions based on the resolution value

    Arguments:
        resolution {int} -- The triangle resolution specified by the user
        key {coord} -- The centre point of the circle

    Returns:
        list of coords -- A list of coord objects which make up the circle division
    """
    r = volume - 1
    angle = 0
    connectList = []
    finalConnect = []

    for i in range(0, res):

        # create an angle between 0 and 2pi that is split evenly by the resolution number
        angle = i * (6.28 / res)

        # calculate new x and y coordinates that meet the angle specified.
        if axis == 'x':
            x = int(key.get_x() + r * math.cos(angle))
            y = int(key.get_y() + r * math.sin(angle))
            connectList.append(coords(x, y, -volume))
        elif axis == 'z':
            x = int(key.get_x() + r * math.cos(angle))
            z = int(key.get_z() + r * math.sin(angle))
            connectList.append(coords(x, 0, z))
    return connectList


def sphere(resolution, mesh, vol):
    """Creates a sphere
    This function will create a sphere

    Arguments:
        resolution {int} -- The number of triangles to create
        mesh {string} -- The type of mesh to create

    Returns:
        List -- A dictionary where each key is a coord object, and it maps to a list of coord objects
        List -- A matrix which contains coord objects for each point of the sphere
    """
    points, angles = circleCoords(vol, 0, vol, 'x', resolution, vol)
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

    test = []

    if mesh == "tri":
        test = connectCircle(resolution, coordSet[0], 'x', matrix, vol)
        connections[coordSet[0]] = test
    elif mesh == "poly":
        connections = {}
    else:
        print("not a valid mesh")
        sys.exit(1)

    newMatrix = matrix + test
    xTransform(newMatrix, angle)

    for k in newMatrix:
        k.set_x(k.xCoord+300)
        k.set_y(k.yCoord+400)
        k.set_z(k.zCoord+400)

    return connections, newMatrix


def cone(res, mesh, vol):
    """Creates a cone

    This funciton will create a mesh of a cone

    Arguments:
        res {[type]} -- The number of triangles to create
        mesh {[type]} -- the type of mesh to create.
    """
    points, angles = circleCoords(vol, -vol, vol, 'z', res, vol)
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

    test = []

    finalConnect = []

    if mesh == "tri":
        test = connectCircle(res, coordSet[0], 'z', matrix, volume)
        for k in test:
            nearest = min(matrix, key=lambda x: (math.sqrt((k.get_x() - x.get_x())**2 + (k.get_y() - x.get_y())**2 + (k.get_z() - x.get_z())**2)))
            finalConnect.append(nearest)

        newConnect = finalConnect

        connections[coordSet[0]] = finalConnect
        connections[coordSet[1]] = newConnect

        newMatrix = matrix
    else:
        print("not a valid mesh")
        sys.exit(1)

    angle = float(input("What angle (in radians) do you wish to rotate on the x axis by?"))

    xTransform(newMatrix, angle)

    angle = float(input("What angle (in radians) do you wish to rotate on the y axis by?"))

    yTransform(newMatrix, angle)

    angle = float(input("What angle (in radians) do you wish to rotate on the z axis by?"))

    yTransform(newMatrix, angle)

    # xTransform(finalConnect, angle)

    for k in newMatrix:
        k.set_x(k.xCoord + 200)
        k.set_y(k.yCoord + 200)
        k.set_z(k.zCoord + 200)

    return connections, newMatrix



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
        print("not a valid mesh")
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
        k.set_x(k.xCoord + 300)
        k.set_y(k.yCoord + 400)
        k.set_z(k.zCoord + 400)



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


    if len(sys.argv) != 6:
        print("not enough arguments")
        sys.exit(1)

    angle = float(sys.argv[1])
    shape = sys.argv[2]
    mesh = sys.argv[3]
    resolution = int(sys.argv[4])
    volume = int(sys.argv[5])

    # redirect to appropriate algorithm for the shape
    if shape == "cube":
        connections, matrix = cube(resolution, mesh)
    elif shape == "sphere":
        connections, matrix = sphere(resolution, mesh, volume)
    elif shape == "cone":
        connections, matrix = cone(resolution, mesh, volume)
    else:
        print("WIP: try using cube or sphere for the shape instead")
        sys.exit(1)

    print(len(matrix))

    # create an image matrix that is empty
    image = [[RGB(0, 0, 0) for j in range(800)] for k in range(800)]



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

    # create the image and save it
    img = Image.fromarray(arr, 'RGB')
    img.save('testing.png')
