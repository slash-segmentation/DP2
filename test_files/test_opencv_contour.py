from numpy import *
import numpy, Image

from opencv import highgui

from opencv import *

from math import *

from matplotlib.pyplot import plot
from matplotlib.pyplot import show

from filters import *

def findMitochondria():
    
    if 0:
        values = []
        domain = arange(-10.0, 10.0, 0.1)
        for x in domain:
            values.append(gaussian(x, 10, 1))
        plot(domain, values)
        show()
    
    for imageIndex in range(34):
        
        #i = Image.open('images/circular_regions.bmp')
        #i = Image.open("C:\\temp\\gradient_is_just_a_blur_function_data_set2_threshold.tif")
    
        #i = Image.open("O:\\images\\HPFcere_vol\\gradient_is_just_a_blur_function_data_set2\\8bit_trimmed\\thresholded\\out%04d.tif" % imageIndex)
        #originalImage = Image.open("O:\\images\\HPFcere_vol\\HPF_rotated_tif\\8bit\\training\\out%04d.tif" % (imageIndex + 3))
        
        i = Image.open("O:\\images\\HPFcere_vol\\HPF_rotated_tif\\median_then_gaussian_8bit_classified_pixels\\tif\\out%04d.tif" % imageIndex) #todo: this should probably use the + 3 also
        originalImage = Image.open("O:\\images\\HPFcere_vol\\HPF_rotated_tif\\median_then_gaussian_8bit\\out%04d.tif" % (imageIndex + 3))
    
        print imageIndex
        
        #numpy_arr = array(numpy.asarray(i))[:,:,0]
        numpy_arr = array(numpy.asarray(i))
        print "numpy_arr", numpy_arr.shape
        numpy_original = array(numpy.asarray(originalImage))
        print "numpy_original", numpy_original.shape
        
        size = cvSize(numpy_arr.shape[0], numpy_arr.shape[1])
    
        smoothedImage = cvCreateImage(size,8,1)
        #smoothedImage = cvCreateMat(numpy_arr.shape[1], numpy_arr.shape[0], CV_8UC1)
        cvSetZero(smoothedImage)
    
        originalImage = cvCreateImage(size, 8, 1)
        contours_image = cvCreateImage(size, 8, 3)
        resultContoursImage = cvCreateImage(size, 8, 3)
        cvSetZero(contours_image)
        
        #print numpy_arr.shape[0]
        #print numpy_arr.shape[1]
        for i in range(numpy_arr.shape[1]):
            for j in range(numpy_arr.shape[0]):
                #print i,j
                #cvmSet(smoothedImage, i, j, int(numpy_arr[i,j])) # this is setting the data incorrectly like it thinks the size of the entry is something other than 8 bits, maybe it thinks 32 bits
    
                #smoothedImage[i,j] = int(numpy_arr[j,i])
                if numpy_arr[j,i] > 100:
                    smoothedImage[i,j] = 1
                
        if 1:
            storage = cvCreateMemStorage(0)
            #print "position 1"
            nb_contours, contours = cvFindContours(smoothedImage,
                                                      storage,
                                                      sizeof_CvContour,
                                                      CV_RETR_LIST,
                                                      CV_CHAIN_APPROX_SIMPLE,
                                                      cvPoint(0,0))
            #print "contours", contours
            if contours == None:
                print "no contours"
                continue
            
            #print "position 2", contours.total
            #contours = cvApproxPoly(contours, sizeof_CvContour,
            #                           storage,
            #                           CV_POLY_APPROX_DP, 1, 1)
    
            #print "position 3"
            _red = cvScalar(0,0,255,0)
            _green = cvScalar(0,255,0,0)
            
            levels = 3
            
            _contours = contours
            
            #print _contours
            #for c in _contours.hrange():
            #    print c
            #    print cvFitEllipse2(c)
    
    
    
            for i in range(numpy_arr.shape[1]):
                for j in range(numpy_arr.shape[0]):
                    contours_image[i,j] = int(numpy_original[j,i])
                    originalImage[i,j] = int(numpy_original[j,i])
                    resultContoursImage[i,j] = int(numpy_original[j,i])
    
            
            cvDrawContours(contours_image, _contours,
                              _red, _green,
                              levels, 1, CV_AA,
                              cvPoint(0, 0))
    
            # This cycle draw all contours and approximate it by ellipses.
            contourIndex = 0
            for c in _contours.hrange():
                count = c.total; # This is number point in contour
                #print c
                if c.v_next != None: print "c.v_next", c.v_next
                if c.v_prev != None: print "c.v_prev", c.v_prev
                
                print c.flags
                c.flags = 1117327884
                #print "c.h_next", c.h_next
                #print "c.h_prev", c.h_prev
    
                size = cvSize(numpy_arr.shape[0], numpy_arr.shape[1])
                contourImage = cvCreateImage(size, 8, 1)
                cvSetZero(contourImage)
                ellipseImage = cvCreateImage(size, 8, 1)
                cvSetZero(ellipseImage)
                andImage = cvCreateImage(size, 8, 1)
                cvSetZero(andImage)
                orImage = cvCreateImage(size, 8, 1)
                cvSetZero(orImage)
                maskedImage = cvCreateImage(size, 8, 1)
                cvSetZero(maskedImage)
    
                resultDisplayImage = cvCreateImage(size, 8, 3)
                cvSetZero(resultDisplayImage)
    
        
                # Number point must be more than or equal to 6 (for cvFitEllipse_32f).        
                if( count < 6 ):
                    continue;
    
                #print cvMatchShapes(c, c, CV_CONTOURS_MATCH_I1)
                
                # Alloc memory for contour point set.
                PointArray = cvCreateMat(1, count, CV_32SC2)
                PointArray2D32f= cvCreateMat( 1, count, CV_32FC2)
                
                # Get contour point set.
                cvCvtSeqToArray(c, PointArray, cvSlice(0, CV_WHOLE_SEQ_END_INDEX));
                
                # Convert CvPoint set to CvBox2D32f set.
                cvConvert( PointArray, PointArray2D32f )
                
                box = CvBox2D()
        
                # Fits ellipse to current contour.
                box = cvFitEllipse2(PointArray2D32f);
                
                # Draw current contour.
                cvDrawContours(contours_image, c, CV_RGB(255,255,255), CV_RGB(255,255,255),0,1,8,cvPoint(0,0));
                cvDrawContours(contourImage, c, CV_RGB(255,255,255), CV_RGB(255,255,255),0,CV_FILLED,8,cvPoint(0,0));
                
                # Convert ellipse data from float to integer representation.
                center = CvPoint()
                size = CvSize()
                center.x = cvRound(box.center.x);
                center.y = cvRound(box.center.y);
                size.width = cvRound(box.size.width*0.5);
                size.height = cvRound(box.size.height*0.5);
                box.angle = -box.angle;
    
                #ellipseWidth = min(size.width, size.height)
                #ellipseHeight = max(size.width, size.height)
                #ellipseAspectRatio = ellipseHeight / ellipseWidth  
    
                #cvEllipse2Poly
                # Alloc memory for contour point set.
                numPolygonPoints = 30
                ellipsePointArray = cvCreateMat(1, numPolygonPoints, CV_32SC2)
                ellipsePointArray2D32f= cvCreateMat( 1, numPolygonPoints, CV_32FC2)
                buffer = [cvPoint(1,1), cvPoint(1,1)]
                #print box.angle
                #cvEllipse2Poly(center, size, int(box.angle), 0, 360, ellipsePointArray2D32f, 1)
                #cvEllipse2Poly(center, size, int(box.angle), 0, 360, buffer, 1)
                
                # Draw ellipse.
                cvEllipse(contours_image, center, size,
                          box.angle, 0, 360,
                          CV_RGB(0,0,255), 1, CV_AA, 0);
                cvEllipse(ellipseImage, center, size,
                          box.angle, 0, 360,
                          CV_RGB(255,255,255), -1, CV_AA, 0);
    
                cvAnd(contourImage, ellipseImage, andImage);
                cvOr(contourImage, ellipseImage, orImage);
    
                andArea = cvSum(andImage)
                orArea = cvSum(orImage)
    
                cvCopy(originalImage, maskedImage, contourImage)
                
                #print orArea
    
                perimeter = cvArcLength(c)
                #print perimeter
    
    
    
                fractionOfOverlap = float(andArea[0]) / float(orArea[0])
    
                amplitude = 1
                overlapValue = gaussian(1.0 - fractionOfOverlap, amplitude, 0.2)
                #perimeterValue = gaussian(abs(74.0 - perimeter), amplitude, 10)
                perimeterValue = gaussian(abs(200.0 - perimeter), amplitude, 150)
                
                #print imageIndex, contourIndex, ". perimeter:", perimeter, "  overlap:", fractionOfOverlap
    
                #color = CV_RGB(int(255.0*overlapValue),int(255.0*perimeterValue),50)
                color = CV_RGB(50,int(255.0*(overlapValue**1)*(perimeterValue**1)),50)
                cvDrawContours(resultDisplayImage, c, color, CV_RGB(255,255,255),0,CV_FILLED,8,cvPoint(0,0));
    
                thickness = 3
                cvDrawContours(resultContoursImage, c, color, CV_RGB(255,255,255),0,thickness,8,cvPoint(0,0));
    
                #cvDrawContours(contours_image, ellipsePointArray, CV_RGB(255,255,255), CV_RGB(128,255,128),0,1,8,cvPoint(0,0))
    
                if 0:
                
                    outputFilename = "c:\\temp\\contour_output\\out%04d_%04d.bmp" % (imageIndex, contourIndex)
                    highgui.cvSaveImage(outputFilename, contourImage)
        
                    outputFilename = "c:\\temp\\contour_output\\out%04d_%04d_and.bmp" % (imageIndex, contourIndex)
                    highgui.cvSaveImage(outputFilename, andImage)
        
                    outputFilename = "c:\\temp\\contour_output\\out%04d_%04d_or.bmp" % (imageIndex, contourIndex)
                    highgui.cvSaveImage(outputFilename, orImage)
        
                    outputFilename = "c:\\temp\\contour_output\\out%04d_%04d_masked.bmp" % (imageIndex, contourIndex)
                    highgui.cvSaveImage(outputFilename, maskedImage)
        
                    outputFilename = "c:\\temp\\contour_output\\out%04d_%04d_display.bmp" % (imageIndex, contourIndex)
                    highgui.cvSaveImage(outputFilename, resultDisplayImage)
    
    
                contourIndex = contourIndex + 1
                
            # Show image. HighGUI use.
            highgui.cvShowImage( "Result", contours_image );
    
        
        if 0:
            highgui.cvNamedWindow("original", 1)
            highgui.cvShowImage("original", smoothedImage)
            
            highgui.cvNamedWindow("contours", 1)
            highgui.cvShowImage("contours", contours_image)
        outputFilename = "c:\\temp\\contour_output\\out%04d.bmp" % imageIndex
        highgui.cvSaveImage(outputFilename, contours_image)
    
        outputFilename = "c:\\temp\\contour_output\\result%04d.bmp" % imageIndex
        highgui.cvSaveImage(outputFilename, resultContoursImage)
    
        #print outputFilename
    print "output written to file stack"
    
    #highgui.cvWaitKey(0)
    
    
findMitochondria()
