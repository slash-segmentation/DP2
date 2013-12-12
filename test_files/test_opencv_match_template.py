from numpy import *
import numpy, Image

from opencv import highgui

from opencv import *

def readImage(filename):

    originalImage = Image.open(filename)
    numpy_original = array(numpy.asarray(originalImage))
    
    cv_image = cvCreateImage(cvSize(numpy_original.shape[0], numpy_original.shape[1]), 8, 1)
    #cv_image = cvCreateMat(numpy_original.shape[0], numpy_original.shape[1], IPL_DEPTH_32F)
    cvSetZero(cv_image)
    for i in range(numpy_original.shape[0]-8):
        for j in range(numpy_original.shape[1]-8):
            cv_image[i,j] = int(numpy_original[i,j])# / 10
            #print numpy_original[i,j]
    return (cv_image, numpy_original.shape)


for imageIndex in range(0, 12):
    contours_image, imageShape = readImage("O:\\images\\HPFcere_vol\\HPF_rotated_tif\\8bit\\out%04d.tif" % imageIndex)

    template, templateShape = readImage("C:\\data\\m\\eclipse_workspace\\blobcenter\\test_files\\data\\vesicle.tif")

    resultShape = (array(imageShape) - array(templateShape)) + 1

    result = cvCreateImage(cvSize(resultShape[0], resultShape[1]), IPL_DEPTH_32F, 1)

    result8bit = cvCreateImage(cvSize(resultShape[0], resultShape[1]), 8, 1)


    cvMatchTemplate(contours_image, template, result, CV_TM_CCOEFF);
    
    cvConvertScale(result, result8bit, .01)
    
#    originalImage = Image.open("O:\\images\\HPFcere_vol\\HPF_rotated_tif\\8bit\\out%04d.tif" % imageIndex)
#    #print originalImage
#    numpy_original = array(numpy.asarray(originalImage))
#    
#    #cv_matrix = cvCreateMat(numpy_arr.shape[0], numpy_arr.shape[1], CV_8UC1)
#    
#    print numpy_original.shape
#    contours_image = cvCreateImage(cvSize(numpy_original.shape[0], numpy_original.shape[1]), 8, 3)
#    cvSetZero(contours_image)
#    for i in range(numpy_original.shape[0]-8):
#        for j in range(numpy_original.shape[1]-8):
#            contours_image[i,j] = int(numpy_original[i,j])
    
    #storage = cvCreateMemStorage(0)
    #_red = cvScalar(0,0,255,0)
    #_green = cvScalar(0,255,0,0)
    
    #_contours = contours
    



    

        
    # Show image. HighGUI use.
    #highgui.cvShowImage( "Result", contours_image );

    
    outputFilename = "c:\\temp\\template\\out%04d.bmp" % imageIndex
    highgui.cvSaveImage(outputFilename, result8bit)
    #highgui.cvSaveImage(outputFilename, contours_image)
    #print outputFilename
print "output written to file stack"

highgui.cvWaitKey(0)


