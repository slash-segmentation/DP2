#http://www.scipy.org/Cookbook/Interpolation

from scipy import ogrid, sin, mgrid, ndimage, array

import numpy

inputShape = (3, 4)
factor = (2, 2)

for number in inputShape:
    if type(number) != type(1):
        raise Exception, "Non-integer %s used. Please use an integer." % number

for number in factor:
    if type(number) != type(1):
        raise Exception, "Non-integer %s used. Please use an integer." % number


x,y = ogrid[-1:1:inputShape[0]*1j,-1:1:inputShape[1]*1j]
fvals = sin(x)*sin(y)
Nx = ((inputShape[0]-1)*factor[0]+1) # new number of samples in x direction
Ny = ((inputShape[1]-1)*factor[1]+1) # new number of samples in y direction

#ivals, jvals = mgrid[0:Nx-1:Nx*1j, 0:Ny-1:Ny*1j]

ivals, jvals = mgrid[0:inputShape[0]-1:Nx*1j, 0:inputShape[1]-1:Ny*1j]


#newx,newy = mgrid[-1:1:Nx*1j,-1:1:Ny*1j]
#x0 = x[0,0]
#y0 = y[0,0]
#dx = x[1,0] - x0
#dy = y[0,1] - y0

# make indicies go from 0 to n-1 considering n is number of rows or cols in the x matrix (or the y matrix)
#ivals = (newx - x0)/dx
#jvals = (newy - y0)/dy

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
#print numpy.float(newf)
print newf

    
    
