from numpy import *
import numpy, Image

from opencv import highgui

#import opencv.cv
from opencv.cv import *

i = Image.open('images/circular_regions.bmp')
#a = numpy.asarray(i) # a is readonly
#i = Image.fromarray(a)

#numpy_arr = ones((10,10))

numpy_arr = array(numpy.asarray(i))

from opencv.adaptors import NumPy2Ipl, Numeric
numericArray = Numeric.array(numpy_arr).astype(Numeric.Float32)
print numericArray
cv_img = NumPy2Ipl(numericArray)
#cv_img = NumPy2Ipl(Numeric.array(numpy_arr).astype(Numeric.UInt8))

#print numpy_arr
#print numpy_arr.min()
#print numpy_arr.max()

#cv_img = opencv.cv.cvLoadImage('images/circular_regions_small.bmp')
#cv_img = highgui.cvLoadImage('images/circular_regions_small.bmp')


for i in range(numpy_arr.shape[0]):
    for j in range(numpy_arr.shape[1]):
        print "cv", cvGet2D(cv_img, i, j)

#pil_img = NumPy2PIL(numericArray)
#for i in range(numpy_arr.shape[0]):
#    for j in range(numpy_arr.shape[1]):
#        print "PIL", pil_img.getpixel(i, j)

cv_img2 = cvCreateImage(cvSize(numpy_arr.shape[0], numpy_arr.shape[1]),IPL_DEPTH_32F,1)
print numpy_arr.shape[0]
print numpy_arr.shape[1]
for i in range(numpy_arr.shape[0]):
#for i in range(1):
    for j in range(numpy_arr.shape[1]):
        #print "numpy", i, ",", j, " ", numpy_arr[i,j]
        #s = cvScalar()
        #cvSet2D(cv_img2, i, j, float(numpy_arr[i,j]))
        #cv_img2[i,j] = numpy_arr[i,j]
        #pass
        cvmSet(cv_img2, i, j, float(numpy_arr[i,j]))

#cvSet2D(cv_img2, 0, 0, double(numpy_arr[i,j]))

if 0:
    for i in range(numpy_arr.shape[0]):
        for j in range(numpy_arr.shape[1]):
            #print "cv2", cvGet2D(cv_img2, i, j)
            print "cv2", cvmGet(cv_img2, i, j)


highgui.cvNamedWindow("original", 1)
highgui.cvShowImage("original", cv_img2)
highgui.cvWaitKey(0)


