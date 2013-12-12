from point_set import *
from numpy import *

pointList = []

if 0:
    # 410 megs
    for i in range(1000 * 1000 * 1):
        pointList.append(LabeledPoint((0,0,0)))

if 0:
    # 20 megs for * 1
    # 67 megs for * 4
    for i in range(1000 * 1000 * 4):
        pointList.append((0,0,0))

class LabeledPointSmall:
    def __init__(self, location):
        self.loc = location


if 0:
    # 811 megs
    for i in range(1000 * 1000 * 4):
        pointList.append(LabeledPointSmall((0,0,0)))


if 1:
    # 416 megs
    for i in range(1000 * 1000 * 4):
        pointList.append(array((0,0,0)))
    

while True:
    print "loop"

