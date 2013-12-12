from data_viewer import *
from volume3d_util import *
from contour_processing import *
import cv

inputStack = "o:\\images\\neuropil\\data"

outputFolder = "o:\\trace_output"

box = Box()
box.cornerA = [0, 0, 200]
box.cornerB = [700, 600, 210]
v = loadImageStack(inputStack, box)

writeStack(outputFolder, v)

s = v.shape
print "shape", s

binaryImage = cv.CreateImage((s[0], s[1]), 8, 1)
contoursImage = cv.CreateImage((s[0], s[1]), 8, 3)

cv.SetZero(binaryImage)

for i in range(0, 700):
    for j in range(0, 600):
        if v[i, j, 0] < 128:
            binaryImage[j, i] = 1
        else:
            binaryImage[j, i] = 0

storage = cv.CreateMemStorage(0)
contours = cv.FindContours(binaryImage, storage, cv.CV_RETR_TREE, cv.CV_CHAIN_APPROX_SIMPLE, (0,0))

for contour in contours:
    print contour

print "draw contours"
cv.DrawContours(contoursImage, contours, (0,0,255,0), (0,255,0,0), 3, 1, cv.CV_AA, (0,0))

#cv.NamedWindow("image", 1)
cv.ShowImage("contours", contoursImage)
cv.WaitKey(0)
# find contour centers for all seed points
# connect the centers with dijkstra

