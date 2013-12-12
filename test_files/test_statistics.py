#sort list to get minimum, 0.25-quantile, median, 0.75-quantile, and the maximum

from numpy import *
import numpy

#test = array([10,10,10,40,50,60,70,80,90,100,110,120])

test = array([40,50,100,110,10,90,10,120,80,60,70,10])

#print array.sort()
#print test.sort()
test.sort()
print test


print "minimum"
print test.min()

print "minimum"
print test[0]

print "0.25 quantile"
#print test[(len(test)-1)]

print test[(len(test)/4)-1]
print test[(2*len(test)/4)-1]
print test[(3*len(test)/4)-1]
print test[(4*len(test)/4)-1]

s = set([3,2,1])
a = array(s)
print a
print numpy.array(s)

#print a[0]

#----------------------------
import statistics
v = array([1,6,4,-3,3,3,4,-30,0,2,5])
print numpy.std(v)
#print statistics.moment(v, 1)
#print statistics.moment(v, 2)
print statistics.moments(v)

