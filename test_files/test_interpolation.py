#http://www.scipy.org/Cookbook/Interpolation

from scipy import ogrid, sin, mgrid, ndimage, array

import numpy

x,y = ogrid[-1:1:3j,-1:1:3j]
fvals = sin(x)*sin(y)
newx,newy = mgrid[-1:1:6j,-1:1:6j]
x0 = x[0,0]
y0 = y[0,0]
dx = x[1,0] - x0
dy = y[0,1] - y0

# make indicies go from 0 to n-1 considering n is number of rows or cols in the x matrix (or the y matrix)
ivals = (newx - x0)/dx
jvals = (newy - y0)/dy

coords = array([ivals, jvals])
#coords1 = mgrid[0:2:6j,0:2:6j] #this works with ndimage.map_coordinates
#coords1 = ogrid[0:2:6j,0:2:6j] #this does not work with ndimage.map_coordinates

print "fvals"
print fvals
#print "coords1"
#print coords1
print "-----------"
#print numpy.abs(coords1[0])
newf = ndimage.map_coordinates(fvals, coords)
#newf = ndimage.map_coordinates(fvals, coords1)
#newf = ndimage.map_coordinates(fvals, numpy.abs(coords1))

print "newf"
print newf

if 0:
    
    print newx.shape
    print newy.shape
    
    
    #print mgrid[1:3,1:3,1:3]
    
    xtest,ytest = mgrid[1:3,1:3]
    
    print 'xtest'
    print xtest
    print 'ytest'
    print ytest
    
    values = array([[50,60],[70,80]])
    coordinates = array([[2,3,4,5],[0,1,2,3]])
    print coordinates
    print '------------------'
    print ndimage.map_coordinates(values, coordinates)
    
    # checking how output is arranged into rows and colums, what coordinate is for rows and what is for columns 
    print 'zeros'
    #a = numpy.zeros(3,4)
    a = numpy.zeros((3,5))
    print a
    
    
