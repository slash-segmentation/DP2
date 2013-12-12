from data_viewer import *
from volume3d_util import *
from contour_processing import *
import cv
from best_path import *

inputStack = "o:\\images\\neuropil\\seg"

outputFolder = "o:\\trace_output"

box = Box()
box.cornerA = [0, 0, 200]
box.cornerB = [700, 500, 210]
v = loadImageStack(inputStack, box)

writeStack(outputFolder, v)

s = v.shape
print "shape", s

binaryImage = cv.CreateImage((s[0], s[1]), 8, 1)
contoursImage = cv.CreateImage((s[0], s[1]), 8, 3)

cv.SetZero(binaryImage)

def toOpenCV(array):
    s = array.shape
    openCVImage = cv.CreateImage((s[0], s[1]), 8, 1)

    for i in range(0, s[0]):
        for j in range(0, s[1]):
            openCVImage[j, i] = array[i, j]

    return openCVImage


for i in range(0, s[0]):
    for j in range(0, s[1]):
        if v[i, j, 0] < 128:
            binaryImage[j, i] = 1
        else:
            binaryImage[j, i] = 0

storage = cv.CreateMemStorage(0)
contours1 = cv.FindContours(binaryImage, storage, cv.CV_RETR_LIST, cv.CV_CHAIN_APPROX_SIMPLE, (0,0))
contours = contour_iterator(contours1)

def rectCenter(openCVRect):
    rect = openCVRect
    rect = cv.BoundingRect(contour)
    #print rect
    x = (rect[0] + rect[2]/2.0)
    y = (rect[1] + rect[3]/2.0)
    return (x, y)

#print contours1.h_next()

print "draw contours"
cv.DrawContours(contoursImage, contours1, (0,0,255,0), (0,255,0,0), 3, 1, cv.CV_AA, (0,0))

for contour in contours:
    center = rectCenter(contour)
    cv.Circle(contoursImage, center, 5, (0,255,255,0))

def makeGraph(volume):
    graph = {}
    step = [10, 10, 1]
    volumeSize = volume.shape
    limit = [None, None, None]
    for coordinate in range(0, 3):
        limit[coordinate] = volumeSize[coordinate]/step[coordinate]

    for x in range(0, limit[0]):
        for y in range(0, limit[1]):
            for z in range(0, limit[2]):
                volx = x * step[0]
                voly = y * step[1]
                volz = z * step[2]
                graph[(x,y,z)] = {}
                if x != limit[0]-1:
                    graph[(x,y,z)][(x+1,y,z)] = volume[volx+step[0],voly,volz]
                if x != 0:
                    graph[(x,y,z)][(x-1,y,z)] = volume[volx-step[0],voly,volz]
                if y != limit[1]-1:
                    graph[(x,y,z)][(x,y+1,z)] = volume[volx,voly+step[1],volz]
                if y != 0:
                    graph[(x,y,z)][(x,y-1,z)] = volume[volx,voly-step[1],volz]
                if z != limit[2]-1:
                    graph[(x,y,z)][(x,y,z+1)] = volume[volx,voly,volz+step[2]]
                if z != 0:
                    graph[(x,y,z)][(x,y,z-1)] = volume[volx,voly,volz-step[2]]


    """
    for x in range(0+xStep, volumeSize[0]-xStep, xStep):
        for y in range(0+yStep, volumeSize[1]-yStep, yStep):
            for z in range(0+1, volumeSize[2]-1):
                graph[(x,y,z)] = {}
                graph[(x,y,z)][(x+xStep,y,z)] = volume[x+xStep,y,z]
                graph[(x,y,z)][(x-xStep,y,z)] = volume[x-xStep,y,z]
                graph[(x,y,z)][(x,y+yStep,z)] = volume[x,y+yStep,z]
                graph[(x,y,z)][(x,y-yStep,z)] = volume[x,y-yStep,z]
                graph[(x,y,z)][(x,y,z+1)] = volume[x,y,z+1]
                graph[(x,y,z)][(x,y,z-1)] = volume[x,y,z-1]
    """
    return graph

graph = makeGraph(v)

path = shortestPath1(graph, (10, 10, 1), (10, 10, 8))

print path

cv.ShowImage("contours", contoursImage)

pointsGroupedByZ = {}
for point in path:
    z = point[2]
    #print point
    if not(z in pointsGroupedByZ):
        pointsGroupedByZ[z] = []
    pointsGroupedByZ[z].append(point)

print pointsGroupedByZ

# for each slice, show the path points
for z in range(0, 10):

    # create image
    #sliceImage = cv.CreateImage((s[0], s[1]), 8, 3)
    sliceImage = toOpenCV(v[:,:,z])

    # plot points for this slice
    if z in pointsGroupedByZ:
        for point in pointsGroupedByZ[z]:
            #print point
            cv.Circle(sliceImage, (point[0], point[1]), 6, (0,255,0,0))

    # write slice to file
    fileName = os.path.join(outputFolder, "path%03d.png" % z)
    print fileName
    cv.SaveImage(fileName, sliceImage)


cv.SaveImage(os.path.join(outputFolder, "output.png"), contoursImage)
#cv.WaitKey(0)
# find contour centers for all seed points
# connect the centers with dijkstra






