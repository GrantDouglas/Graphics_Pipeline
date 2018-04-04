#!/usr/bin/python3


import math, time, sys, array, os, copy, itertools
from itertools import cycle
from operator import attrgetter
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
        return [self.xCoord, self.yCoord, self.zCoord]

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

class polygon:

    def __init__(self, p1, p2, p3):
        self.point1 = p1
        self.point2 = p2
        self.point3 = p3

    def values(self):
        return [self.point1.send_vals(), self.point2.send_vals(), self.point3.send_vals()]


class squarePoly:

    def __init__(self, p1, p2, p3, p4):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4



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


def translate(points, factor):

    for i in points:
        x = i.get_x()
        y = i.get_y()
        z = i.get_z()

        newx = x - factor
        newy = y - factor
        newz = z - factor

        i.set_x(newx)
        i.set_y(newy)
        i.set_z(newz)


def rotation(points, xangle, yangle, zangle):

    for i in points:
        x = i.get_x()
        y = i.get_y()
        z = i.get_z()

        newx = int(x * math.cos(zangle) - y * math.sin(zangle))
        newy = int(x * math.sin(zangle) + y * math.cos(zangle))

        i.set_x(newx)
        i.set_y(newy)

    for i in points:
        x = i.get_x()
        z = i.get_z()

        newx = int(x * math.cos(yangle) + z * math.sin(yangle))
        newz = int(z * math.cos(yangle) - x * math.sin(yangle))

        i.set_x(newx)
        i.set_z(newz)

    for i in points:
        y = i.get_y()
        z = i.get_z()

        newy = int(y * math.cos(xangle) - z * math.sin(xangle))
        newz = int(y * math.sin(xangle) + z * math.cos(xangle))

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


def dotProduct(v1, v2):
    return sum(i * j for i, j in zip(v1, v2))


def vectorSub(p1, p2):
    return [a - b for a, b in zip(p1, p2)]


def vectorAdd(p1, p2):
    return [a + b for a, b in zip(p1, p2)]


def crossProduct(v1, v2):
    val1 = v1[1] * v2[2] - v1[2] * v1[1]
    val2 = v1[2] * v2[0] - v1[0] * v2[2]
    val3 = v1[0] * v2[1] - v1[1] * v2[0]
    return [val1, val2, val3]


def connect(matrix, key, gap, res):
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
        if (x.get_x() - key.get_x() == 0 and x.get_z() == key.get_z())\
        or (x.get_y() - key.get_y() == 0 and x.get_z() == key.get_z())\
        or (x.get_z() - key.get_z() != 0 and x.get_y() == key.get_y() and x.get_x() == key.get_x()):
            connectionPoints.append(x)

    origin = matrix[1]


    for x in matrix:
        if (x.get_x() == key.get_y() and x.get_y() == key.get_x() and x.get_z() == key.get_z())\
        or (x.get_z() == key.get_x() and x.get_x() == key.get_z() and x.get_y() == key.get_y())\
        or (x.get_z() == key.get_y() and x.get_y() == key.get_z() and x.get_x() == key.get_x()):

            connectionPoints.append(x)

    return connectionPoints


def vector(point1, point2):
    x = point2.get_x() - point1.get_x()
    y = point2.get_y() - point1.get_y()
    z = point2.get_z() - point1.get_z()

    vec = [x, y, z]

    return vec


def cylinder(resolution, mesh, vol, isScene, xangle, yangle, zangle):
    """Creates a cylinder
    This function will create a cylinder

    Arguments:
        resolution {int} -- The number of triangles to create
        mesh {string} -- The type of mesh to create

    Returns:
        List -- A dictionary where each key is a coord object, and it maps to a list of coord objects
        List -- A matrix which contains coord objects for each point of the cylinder
    """

    points = []
    connections = {}
    faceDict = {}
    test = []
    finalConnect = []
    polyList = []

    # define midpoints of the circles
    points.append(coords(0, vol, -vol))
    points.append(coords(0, 0, 0))

    # create circles that define the cylinder
    testList = newCirc(resolution, 'z', vol)
    tempList = copy.deepcopy(testList)

    # adjust the second circle to be further out
    for k in tempList:
        k.set_y(k.get_y() + vol)
        k.set_z(k.get_z() - vol)


    newList = points + testList + tempList

    # create a list of points which define each circle
    connList1 = points + testList
    connList2 = points + tempList


    if mesh == "tri":

       # connect all points in first circle of cylinder
        for first, second in zip(connList1[2:], connList1[3:]):
            connections[first] = [connList1[1], second]
            connections[second] = [connList1[1], first]

            polyList.append(polygon(connList1[1], first, second))


        connections[connList1[-1]] = [connList1[2], connList1[1]]

        polyList.append(polygon(connList1[1], connList1[-1], connList1[2]))

        # connect all points in second circle of cylinder
        for first, second in zip(connList2[2:], connList2[3:]):
            connections[first] = [connList2[0], second]
            connections[second] = [connList2[0], first]

            polyList.append(polygon(connList2[0], first, second))

        connections[connList2[-1]] = [connList2[2], connList2[0]]

        polyList.append(polygon(connList2[0], connList2[-1], connList2[2]))

        # print(len(polyList))

        # connect all points in both circles to each other based on index
        for k in range(2, len(connList1)):
            num = k + 1
            if num >= len(connList1):
                num = 2

            print(len(connList1), num)

            polyList.append(polygon(connList1[k], connList1[num], connList2[num]))
            polyList.append(polygon(connList1[k], connList2[k], connList2[num]))
            connections[connList1[k]].append(connList2[k])

        print(len(polyList))

        newMatrix = newList
    else:
        print("not a valid mesh")
        sys.exit(1)


    if isScene:
        for k in newMatrix:
            k.set_x(k.xCoord + 250 + (vol/4))
            k.set_y(k.yCoord + 225 + (vol/4))
            k.set_z(k.zCoord + 450 - vol)

    else:

        angle = float(input("What angle (in radians) do you wish to rotate the cylinder on the x axis by?"))
        xTransform(newMatrix, angle)

        angle = float(input("What angle (in radians) do you wish to rotate the cylinder on the y axis by?"))
        yTransform(newMatrix, angle)

        angle = float(input("What angle (in radians) do you wish to rotate the cylinder on the z axis by?"))
        zTransform(newMatrix, angle)

        for k in newMatrix:
            k.set_x(k.xCoord+300)
            k.set_y(k.yCoord+400)
            k.set_z(k.zCoord+400)

    return connections, newMatrix


def newCirc(res, axis, vol):


    r = volume - 1
    angle = 0
    connectList = []
    finalConnect = []

    for i in range(0, res):

        # create an angle between 0 and 2pi that is split evenly by the resolution number
        angle = i * (6.28 / res)

        # calculate new x and y coordinates that meet the angle specified.
        if axis == 'x':
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            connectList.append(coords(x, y, -volume))
        elif axis == 'z':
            x = r * math.cos(angle)
            z = r * math.sin(angle)
            connectList.append(coords(x, 0, z))
    return connectList




def cone(res, mesh, vol, isScene, xangle, yangle, zangle):
    """Creates a cone

    This funciton will create a mesh of a cone

    Arguments:
        res {[type]} -- The number of triangles to create
        mesh {[type]} -- the type of mesh to create.
    """

    points = []
    connections = {}
    faceDict = {}
    test = []
    finalConnect = []
    polyList = []
    count = 0

    # define midpoint of circle, and the tip of the cone

    points.append(coords(0, vol, -vol))
    points.append(coords(0, 0, 0))

    # create the circle
    testList = newCirc(res, 'z', vol)
    newList = points + testList


    if mesh == "tri":

        # connect all points in circle and point to each other
        for first, second in zip(newList[2:], newList[3:]):
            connections[first] = [newList[0], newList[1], second]
            connections[second] = [newList[0], newList[1], first]

            # testing polygon
            polyList.append(polygon(newList[0], first, second))
            polyList.append(polygon(newList[1], first, second))


        connections[newList[-1]] = [newList[0], newList[2], newList[1]]


        # testing polygon
        polyList.append(polygon(newList[0], newList[-1], newList[2]))
        polyList.append(polygon(newList[1], newList[-1], newList[2]))

        newMatrix = newList
    else:
        print("not a valid mesh")
        sys.exit(1)


    # for k in polyList:
    #     print(k.point1.send_vals(), k.point2.send_vals(), k.point3.send_vals())


    if isScene:

        for k in newMatrix:
            k.set_x(k.xCoord + 400-vol)
            k.set_y(k.yCoord + 500+2*(vol/2))
            k.set_z(k.zCoord + 550+vol/4)
    else:

        angle = float(input("What angle (in radians) do you wish to rotate the cone on the x axis by?"))
        xTransform(newMatrix, angle)

        angle = float(input("What angle (in radians) do you wish to rotate the cone on the y axis by?"))
        yTransform(newMatrix, angle)

        angle = float(input("What angle (in radians) do you wish to rotate the cone on the z axis by?"))
        zTransform(newMatrix, angle)

        for k in newMatrix:
            k.set_x(k.xCoord + 200)
            k.set_y(k.yCoord + 200)
            k.set_z(k.zCoord + 200)

    return connections, newMatrix, faceDict


def cube(res, mesh, isScene, xangle, yangle, zangle, vol):
    """Create a cube

    This function will create the points which make up a cube

    Arguments:
        res {int} -- The resolution of the faces on the cube
        mesh {string} -- the mesh type of the cube

   Returns:
        List -- A dictionary where each key is a coord object, and it maps to a list of coord objects
        List -- A matrix which contains coord objects for each point of the cylinder
    """
    points = [
        [vol, vol, -vol],
        [-vol, vol, -vol],
        [vol, -vol, -vol],
        [-vol, -vol, -vol],
        [vol, vol, vol],
        [-vol, vol, vol],
        [vol, -vol, vol],
        [-vol, -vol, vol]
        ]
    cubeList = []
    faceDict = {}
    finalPoints = []
    matrix = []
    connections = {}
    count = 0

    polyList = []

    polyList.append(squarePoly(points[0], points[1], points[3], points[2]))
    polyList.append(squarePoly(points[4], points[5], points[1], points[0]))
    polyList.append(squarePoly(points[4], points[0], points[2], points[6]))
    polyList.append(squarePoly(points[5], points[4], points[6], points[7]))
    polyList.append(squarePoly(points[1], points[5], points[7], points[3]))
    polyList.append(squarePoly(points[2], points[3], points[7], points[6]))

    test = newGrid(res, points, vol, polyList)

    # create mesh based on connections
    if mesh == "tri":
        triangGrid, gap = grid(res, points, vol)
        newPoints = triangGrid + points
    elif mesh == "poly":
        newPoints = points
    else:
        print("not a valid mesh")
        sys.exit(1)

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
        connections[key] = connect(coordList, key, gap, resolution)

    for k in points:
        temp = 0
        for j in coordSet:
            if k == j.send_vals():
                stuff = True
                temp = j
        if stuff == True:
            cubeList.append(temp)

    # all faces that make up the cube, given corner points
    faceDict[0] = [cubeList[0], cubeList[1], cubeList[3], cubeList[2]]
    faceDict[1] = [cubeList[4], cubeList[5], cubeList[1], cubeList[0]]
    faceDict[2] = [cubeList[4], cubeList[0], cubeList[2], cubeList[6]]
    faceDict[3] = [cubeList[5], cubeList[4], cubeList[6], cubeList[7]]
    faceDict[4] = [cubeList[1], cubeList[5], cubeList[7], cubeList[3]]
    faceDict[5] = [cubeList[2], cubeList[3], cubeList[7], cubeList[6]]

    if isScene:
        for k in coordList:
            k.set_x(k.xCoord + 400)
            k.set_y(k.yCoord + 500)
            k.set_z(k.zCoord + 400)

    else:
        # transform the x and y coordinates to make 3d shape more clear

        angle = float(input("What angle (in radians) do you wish to rotate the cube on the x axis by?"))
        xTransform(coordList, angle)

        angle = float(input("What angle (in radians) do you wish to rotate the cube on the y axis by?"))
        yTransform(coordList, angle)

        angle = float(input("What angle (in radians) do you wish to rotate the cube on the z axis by?"))
        zTransform(coordList, angle)

        # move the square to the middle of the image for a cleaner look
        for k in coordList:
            k.set_x(k.xCoord + 300)
            k.set_y(k.yCoord + 400)
            k.set_z(k.zCoord + 400)


    return connections, matrix, faceDict


def newGrid(res, points, vol, squares):

    polyList = []

    # print(squares)

    for k in squares:
        p1 = k.p1
        p2 = k.p2
        p3 = k.p3
        p4 = k.p4

        lists = []


        if p1[0] == p2[0] == p3[0] == p4[0]:
            gap = int((max(p1[1], p2[1], p3[1], p4[1]) - min(p1[1], p2[1], p3[1], p4[1])) / res)
            start = min(p1[1], p2[1], p3[1], p4[1])
            end = max(p1[1], p2[1], p3[1], p4[1])
            print("on x axis", gap)

            for l in range(start, end+1, gap):
                sampleList = []
                for m in range(start, end+1, gap):

                    sample = coords(p1[0], m, l)
                    sampleList.append(sample)

                lists.append(sampleList)

            for l in range(1, res+1):
                list1 = lists[l-1]
                list2 = lists[l]

                for m in range(1, res+1):

                    polyList.append(polygon(list1[m-1], list1[m], list2[m]))
                    polyList.append(polygon(list1[m-1], list2[m-1], list2[m]))


        elif p1[1] == p2[1] == p3[1] == p4[1]:
            gap = int((max(p1[2], p2[2], p3[2], p4[2]) - min(p1[2], p2[2], p3[2], p4[2])) / res)
            start = min(p1[2], p2[2], p3[2], p4[2])
            end = max(p1[2], p2[2], p3[2], p4[2])
            print("on y axis", gap)

            for l in range(start, end+1, gap):
                sampleList = []
                for m in range(start, end+1, gap):

                    sample = coords(m, p1[1], l)
                    sampleList.append(sample)

                lists.append(sampleList)

            for l in range(1, res+1):
                list1 = lists[l-1]
                list2 = lists[l]

                for m in range(1, res+1):

                    polyList.append(polygon(list1[m-1], list1[m], list2[m]))
                    polyList.append(polygon(list1[m-1], list2[m-1], list2[m]))

        elif p1[2] == p2[2] == p3[2] == p4[2]:
            gap = int((max(p1[0], p2[0], p3[0], p4[0]) - min(p1[0], p2[0], p3[0], p4[0])) / res)

            start = min(p1[0], p2[0], p3[0], p4[0])
            end = max(p1[0], p2[0], p3[0], p4[0])
            print("on z axis", gap)

            # grid triangulation on z axis faces
            for l in range(start, end+1, gap):
                sampleList = []
                for m in range(start, end+1, gap):

                    sample = coords(m, l, p1[2])
                    sampleList.append(sample)

                lists.append(sampleList)

            for l in range(1, res+1):
                list1 = lists[l-1]
                list2 = lists[l]

                for m in range(1, res+1):

                    polyList.append(polygon(list1[m-1], list1[m], list2[m]))
                    polyList.append(polygon(list1[m-1], list2[m-1], list2[m]))

        print(len(polyList))







    # check cube poly for the points
    # check which axis the points are on
    # for each column
    # draw the row
    # store each row
    #
    # for each row in the row list
    # compare curr list with next list

    return polyList


def grid(resolution, points, vol):
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

    print(len(newFinal))

    return newFinal, gap


def matrixVectorMultiply(vector, matrix):

    x = matrix[0][0] * vector[0] + matrix[0][1] * vector[1] + matrix[0][2] * vector[2] + matrix[0][3] * vector[3]
    y = matrix[1][0] * vector[0] + matrix[1][1] * vector[1] + matrix[1][2] * vector[2] + matrix[1][3] * vector[3]
    z = matrix[2][0] * vector[0] + matrix[2][1] * vector[1] + matrix[2][2] * vector[2] + matrix[2][3] * vector[3]
    f = matrix[3][0] * vector[0] + matrix[3][1] * vector[1] + matrix[3][2] * vector[2] + matrix[3][3] * vector[3]

    result = [x, y, z, f]

    return result


def normalized(vector):
    mag = math.sqrt((vector[0])**2 + (vector[1])**2 + (vector[2])**2)
    x = vector[0] / mag
    y = vector[1] / mag
    z = vector[2] / mag

    normVector = [x, y, z]
    return normVector


def viewTransform(pointMatrix):
    zAxis = normalized(vectorSub([500,500,800], [500,500,0]))
    xAxis = normalized(crossProduct([0,1,0], zAxis))
    yAxis = crossProduct(xAxis, zAxis)



    print(yAxis)



def scene(mesh, resolution, volume, isScene):

    cull = False
    clip = False
    HSR = False

    userInput = input("Do you want to use culling? (please enter yes or no)")
    if userInput == "yes" or userInput == "Yes":
        cull = True
    elif userInput == "no" or userInput == "No":
        cull = False
    else:
        print("Not a valid response, Exiting.")
        sys.exit(1)

    if cull == True:
        userInput = input("Do you want to use clipping? (please enter yes or no)")
        if userInput == "yes" or userInput == "Yes":
            clip = True
        elif userInput == "no" or userInput == "No":
            clip = False
        else:
            print("Not a valid response, Exiting.")
            sys.exit(1)

        userInput = input("Do you want to use hidden surface removal? (please enter yes or no)")
        if userInput == "yes" or userInput == "Yes":
            HSR = True
        elif userInput == "no" or userInput == "No":
            HSR = False
        else:
            print("Not a valid response, Exiting.")
            sys.exit(1)

    xangle = float(input("What angle (in radians) do you wish to rotate on the x axis by?"))

    yangle = float(input("What angle (in radians) do you wish to rotate on the y axis by?"))

    zangle = float(input("What angle (in radians) do you wish to rotate on the z axis by?"))

    matricies = []
    connectionsDict = {}

    connections, matrix1, faceDict1 = cube(resolution, mesh, isScene, xangle, yangle, zangle, volume)
    removeWrapping(matrix1)

    connectionsDict.update(connections)


    connections, matrix2 = cylinder(resolution, mesh, volume, isScene, xangle, yangle, zangle)
    removeWrapping(matrix2)

    connectionsDict.update(connections)

    connections, matrix3, faceDict2 = cone(resolution, mesh, volume, isScene, xangle, yangle, zangle)
    removeWrapping(matrix3)

    tempDict = connections

    connectionsDict.update(connections)

    faceDict = {}

    faceDict.update(faceDict2)
    faceDict.update(faceDict1)


    matricies.append(matrix1)
    matricies.append(matrix2)
    matricies.append(matrix3)


    viewTransform(matricies)

    pointDict = {}

    for k in range(0, 6):
        temp = faceDict[k]
        pointDict[k] = []

        if(temp[0].get_x() == temp[1].get_x() == temp[2].get_x() == temp[3].get_x()):

            max_y = max(temp[0].get_y(), temp[1].get_y(), temp[2].get_y(), temp[3].get_y())
            max_z = max(temp[0].get_z(), temp[1].get_z(), temp[2].get_z(), temp[3].get_z())

            min_y = min(temp[0].get_y(), temp[1].get_y(), temp[2].get_y(), temp[3].get_y())
            min_z = min(temp[0].get_z(), temp[1].get_z(), temp[2].get_z(), temp[3].get_z())

            for x in matrix1:
                if min_y <= x.get_y() <= max_y and min_z <= x.get_z() <= max_z and x.get_x() == temp[0].get_x():
                    pointDict[k].append(x)

        elif(temp[0].get_y() == temp[1].get_y() == temp[2].get_y() == temp[3].get_y()):

            max_x = max(temp[0].get_x(), temp[1].get_x(), temp[2].get_x(), temp[3].get_x())
            max_z = max(temp[0].get_z(), temp[1].get_z(), temp[2].get_z(), temp[3].get_z())

            min_x = min(temp[0].get_x(), temp[1].get_x(), temp[2].get_x(), temp[3].get_x())
            min_z = min(temp[0].get_z(), temp[1].get_z(), temp[2].get_z(), temp[3].get_z())

            for x in matrix1:
                if min_x <= x.get_x() <= max_x and min_z <= x.get_z() <= max_z and x.get_y() == temp[0].get_y():
                    pointDict[k].append(x)

        elif(temp[0].get_z() == temp[1].get_z() == temp[2].get_z() == temp[3].get_z()):

            max_x = max(temp[0].get_x(), temp[1].get_x(), temp[2].get_x(), temp[3].get_x())
            max_y = max(temp[0].get_y(), temp[1].get_y(), temp[2].get_y(), temp[3].get_y())

            min_x = min(temp[0].get_x(), temp[1].get_x(), temp[2].get_x(), temp[3].get_x())
            min_y = min(temp[0].get_y(), temp[1].get_y(), temp[2].get_y(), temp[3].get_y())


            for x in matrix1:
                if min_x <= x.get_x() <= max_x and min_y <= x.get_y() <= max_y and x.get_z() == temp[0].get_z():
                    pointDict[k].append(x)

    for k in range(6, resolution*2+6):
        pointDict[k] = []
        for key, v in faceDict2.items():
            for val in v:
                pointDict[k].append(val)

    flattened = [val for sublist in matricies for val in sublist]

    translate(flattened, 500)
    rotation(flattened, xangle, yangle, zangle)
    translate(flattened, -500)

    pointsToRemove = []


    # for key, val in faceDict.items():
    #     print(key, val)

    temp = []

    # for key, val in faceDict.items():
    #     p0 = val[0].send_vals()
    #     p3 = val[3].send_vals()
    #     p2 = val[2].send_vals()


    #     pneg = [p0[0] - 500, p0[1] - 500, p0[2] - 800]

    #     v1 = vectorSub(p3, p0)
    #     v2 = vectorSub(p2, p0)

    #     norm = crossProduct(v2, v1)

    #     result = dotProduct(norm, pneg)

    #     if result < 0:
    #         print(key)

    #         toKeep = pointDict[key]


    #         # TODO: FIX THIS LOOP ITS WRONG (maybe working now)
    #         for x in toKeep:
    #             if x not in temp:
    #                 temp.append(x)

    temp = []



    for k, v in faceDict.items():

        edge1 = (v[1].get_x() - v[0].get_x()) * (v[1].get_y() + v[0].get_y())
        edge2 = (v[2].get_x() - v[1].get_x()) * (v[2].get_y() + v[1].get_y())
        edge3 = (v[0].get_x() - v[2].get_x()) * (v[0].get_y() + v[2].get_y())
        # edge4 = (v[0].get_x() - v[3].get_x()) * (v[0].get_y() + v[3].get_y())

        result = edge1 + edge2 + edge3


        if result < 0:

            for vals in pointDict[k]:
                temp.append(vals)

    for val in temp:
        if val not in tempDict.keys():

            connectionsDict.pop(val, None)




    # newDict = {}

    # keys = set(temp).intersection(set(connectionsDict.keys()))

    # newDict = {k: connectionsDict[k] for k in keys}

    # for key, vals in newDict.items():
    #     newVals = []
    #     for k in vals:
    #         if k in temp:
    #             newVals.append(k)
    #     newDict[key] = newVals


    # print(len(newDict.values()), len(connectionsDict.values()))




    #     if result < 0:
    #         maxX = max(value.get_x() for value in val)
    #         maxY = max(value.get_y() for value in val)
    #         maxZ = max(value.get_z() for value in val)

    #         minX = min(value.get_x() for value in val)
    #         minY = min(value.get_y() for value in val)
    #         minZ = min(value.get_z() for value in val)


    #         for x in matrix1:
    #             if minX <= x.get_x() <= maxX and minY <= x.get_y() <= maxY and minZ <= x.get_z() <= maxZ and x not in pointsToRemove:
    #                 pointsToRemove.append(x)


    # for i in pointsToRemove:
    #     flattened.remove(i)

    # for i in pointsToRemove:
    #     if i in connectionsDict:
    #         del connectionsDict[i]

    removeWrapping(flattened)

    newFlattened = []


    image, matrix4 = imaging(flattened, connectionsDict, "final.png")

    return 0


def spherical(matrix, xAngle, yAngle):
    for i in matrix:
        for j in i:
            r = math.sqrt(j.get_x()**2 + j.get_y()**2 + j.get_z()**2)
            theta = xAngle
            alpha = yAngle

            newX = int(r * math.cos(theta) * math.sin(alpha))
            newY = int(r * math.sin(theta) * math.sin(alpha))
            newZ = int(r * math.cos(alpha))

            j.set_x(newX)
            j.set_y(newY)
            j.set_z(newZ)


def imaging(matrix, connections, name):

    # limitx = max(x[0].get_x() for x in matrix)
    # limity = max(x[1].get_y() for x in matrix)

    # create an image matrix that is empty
    image = [[RGB(0, 0, 0) for j in range(1000)] for k in range(1000)]

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
    img.save(name)

    return arr, newImage


def removeWrapping(matrix):
    for k in matrix:
        if k.get_x() < 0:
            k.set_x(0)
        elif k.get_x() > 900:
            k.set_x(899)
        elif k.get_y() < 0:
            k.set_y(0)
        elif k.get_y() > 900:
            k.set_y(899)


if __name__ == "__main__":

    if len(sys.argv) != 5:
        print("not enough arguments")
        sys.exit(1)


    shape = sys.argv[1]
    mesh = sys.argv[2]
    resolution = int(sys.argv[3])
    volume = int(sys.argv[4])

    # redirect to appropriate algorithm for the shape
    if shape == "cube":
        connections, matrix = cube(resolution, mesh, False, 0, 0, 0, volume)
        removeWrapping(matrix)
        name = "cube.png"
        image = imaging(matrix, connections, name)
    elif shape == "cylinder":
        connections, matrix = cylinder(resolution, mesh, volume, False, 0, 0, 0)
        removeWrapping(matrix)
        name = "cylinder.png"
        image = imaging(matrix, connections, name)
    elif shape == "cone":
        connections, matrix = cone(resolution, mesh, volume, False, 0, 0, 0)
        removeWrapping(matrix)
        name = "cone.png"
        image = imaging(matrix, connections, name)
    elif shape == "scene":
        scene(mesh, resolution, volume, True)
    else:
        print("WIP: try using cube, cylinder, cone, or scene instead")
        sys.exit(1)




