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
        return [self.point1, self.point2, self.point3]


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

        # making the last connection on first circle
        connections[connList1[-1]] = [connList1[2], connList1[1]]
        polyList.append(polygon(connList1[1], connList1[-1], connList1[2]))

        # connect all points in second circle of cylinder
        for first, second in zip(connList2[2:], connList2[3:]):
            connections[first] = [connList2[0], second]
            connections[second] = [connList2[0], first]

            polyList.append(polygon(connList2[0], first, second))


        # Making the last connection on second circle
        connections[connList2[-1]] = [connList2[2], connList2[0]]
        polyList.append(polygon(connList2[0], connList2[-1], connList2[2]))

        # connect all points in both circles to each other based on index
        for k in range(2, len(connList1)):
            num = k + 1
            if num >= len(connList1):
                num = 2

            polyList.append(polygon(connList1[k], connList1[num], connList2[num]))
            polyList.append(polygon(connList1[k], connList2[k], connList2[num]))
            connections[connList1[k]].append(connList2[k])

        newMatrix = newList
    else:
        print("not a valid mesh")
        sys.exit(1)


    # transform the points
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

    return connections, newMatrix, polyList


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

    # translate the points
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

    return connections, newMatrix, polyList


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
    squareList = []
    polyList = []
    coordList = []

    # add square faces to a square face list
    squareList.append(squarePoly(points[0], points[1], points[3], points[2]))
    squareList.append(squarePoly(points[4], points[5], points[1], points[0]))
    squareList.append(squarePoly(points[4], points[0], points[2], points[6]))
    squareList.append(squarePoly(points[5], points[4], points[6], points[7]))
    squareList.append(squarePoly(points[1], points[5], points[7], points[3]))
    squareList.append(squarePoly(points[2], points[3], points[7], points[6]))

    # create the new grid with the triangles within
    polyList = newGrid(res, points, vol, squareList)

    # create a list of all points created
    for k in polyList:
        for l in k.values():
            if l not in coordList:
                coordList.append(l)

    # translate the points
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


    return connections, matrix, polyList


def newGrid(res, points, vol, squares):

    polyList = []

    for k in squares:
        p1 = k.p1
        p2 = k.p2
        p3 = k.p3
        p4 = k.p4

        lists = []

        # The square lies on the x axis
        if p1[0] == p2[0] == p3[0] == p4[0]:
            gap = int((max(p1[1], p2[1], p3[1], p4[1]) - min(p1[1], p2[1], p3[1], p4[1])) / res)
            start = min(p1[1], p2[1], p3[1], p4[1])
            end = max(p1[1], p2[1], p3[1], p4[1])
            

            # grid creation of square surface, storing each square in the row
            for l in range(start, end+1, gap):
                sampleList = []
                for m in range(start, end+1, gap):

                    sample = coords(p1[0], m, l)
                    sampleList.append(sample)

                lists.append(sampleList)

            # compare a row and the next row
            for l in range(1, res+1):
                list1 = lists[l-1]
                list2 = lists[l]

                #  divide the square in the row into 2 triangles
                for m in range(1, res+1):
                    polyList.append(polygon(list1[m-1], list1[m], list2[m]))
                    polyList.append(polygon(list1[m-1], list2[m-1], list2[m]))


        # the square lies on the y axis
        elif p1[1] == p2[1] == p3[1] == p4[1]:

            # create a gap interval based on resolution, and define a start and end point
            gap = int((max(p1[2], p2[2], p3[2], p4[2]) - min(p1[2], p2[2], p3[2], p4[2])) / res)
            start = min(p1[2], p2[2], p3[2], p4[2])
            end = max(p1[2], p2[2], p3[2], p4[2])
           
            # loop from start to end, jumping each gap interval, and store the point into a list
            for l in range(start, end+1, gap):
                sampleList = []
                for m in range(start, end+1, gap):

                    sample = coords(m, p1[1], l)
                    sampleList.append(sample)

                lists.append(sampleList)

            # compare a row and the next row
            for l in range(1, res+1):
                list1 = lists[l-1]
                list2 = lists[l]

                # divide the square in the row into 2 triangles
                for m in range(1, res+1):
                    polyList.append(polygon(list1[m-1], list1[m], list2[m]))
                    polyList.append(polygon(list1[m-1], list2[m-1], list2[m]))


        # the square lies on the z axis
        elif p1[2] == p2[2] == p3[2] == p4[2]:
            gap = int((max(p1[0], p2[0], p3[0], p4[0]) - min(p1[0], p2[0], p3[0], p4[0])) / res)

            start = min(p1[0], p2[0], p3[0], p4[0])
            end = max(p1[0], p2[0], p3[0], p4[0])
            

            # grid triangulation on z axis faces
            for l in range(start, end+1, gap):
                sampleList = []
                for m in range(start, end+1, gap):

                    sample = coords(m, l, p1[2])
                    sampleList.append(sample)

                lists.append(sampleList)

            # compare a row and the next row
            for l in range(1, res+1):
                list1 = lists[l-1]
                list2 = lists[l]

                # divide the square in the row into 2 triangles
                for m in range(1, res+1):
                    polyList.append(polygon(list1[m-1], list1[m], list2[m]))
                    polyList.append(polygon(list1[m-1], list2[m-1], list2[m]))

    return polyList


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
    polygons = []
    connectionsDict = {}


    connections, matrix1, polyList1 = cube(resolution, mesh, isScene, xangle, yangle, zangle, volume)
    removeWrapping(matrix1)
    connectionsDict.update(connections)


    connections, matrix2, polyList2 = cylinder(resolution, mesh, volume, isScene, xangle, yangle, zangle)
    removeWrapping(matrix2)

    connectionsDict.update(connections)

    connections, matrix3, polyList3 = cone(resolution, mesh, volume, isScene, xangle, yangle, zangle)
    removeWrapping(matrix3)

    tempDict = connections

    connectionsDict.update(connections)


    polygons = polyList1 + polyList2 + polyList3

    flattened = []

    # create list of points to apply transformations
    for k in polygons:
        if k.point1 not in flattened:
            flattened.append(k.point1)
        
        if k.point2 not in flattened:
            flattened.append(k.point2)

        if k.point3 not in flattened:
            flattened.append(k.point3)
       
    # transform points
    translate(flattened, 500)
    rotation(flattened, xangle, yangle, zangle)
    translate(flattened, -500)


    # remove any points that are outside of the image bounds
    removeWrapping(flattened)

    image, matrix4 = imaging(flattened, connectionsDict, "final.png", polygons)

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


def imaging(matrix, connections, name, polyList):

    image = [[RGB(0, 0, 0) for j in range(1000)] for k in range(1000)]

    # place a value of 255 on the image where the cube will be
    for i in matrix:
        image[i.get_x()][i.get_y()].cRed = 255
        image[i.get_x()][i.get_y()].cGreen = 255
        image[i.get_x()][i.get_y()].cBlue = 255

    # rasterize each of the polygons
    for val in polyList:
        key = val.values()
        
        # find all combinations of 2 points in 3 point polygon
        new = list(itertools.combinations(key, 2))

        # connect each point pair together, which forms a triangle
        for k in new:
            rasterize(k[0], k[1], image)

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




