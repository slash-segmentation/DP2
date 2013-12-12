
import itk
from numpy import *
from volume3d_util import *

PixelType = itk.RGBPixel[itk.US]
RGBImageType = itk.Image[PixelType, 2]

reader1 = itk.ImageFileReader[itk.Image[itk.F, 2]].New(FileName="data/classified_out0005.png")
image1 = reader1.GetOutput()
reader2 = itk.ImageFileReader[itk.Image[itk.US, 2]].New(FileName="data/classified_out0005.png")
image2 = reader2.GetOutput()
reader3 = itk.ImageFileReader[itk.Image[itk.US, 2]].New(FileName="data/classified_out0005.png")
image3 = reader3.GetOutput()
reader1.Update()
image1.Update()

#composeFilter = itk.ComposeRGBImageFilter[itk.Image[itk.US, 2], RGBImageType].New()
#composeFilter.SetInput1(image1)
#composeFilter.SetInput2(image2)
#composeFilter.SetInput3(image3)
#composeFilter.Update()

#itk.write(image1, "o:/temp/classified_out0005.bmp")
#itk.write(composeFilter.GetOutput(), "o:/temp/compose_test.bmp")

InternalPixelType = itk.F
Dimension = 2
ImageType = itk.Image[InternalPixelType, Dimension]
converter = itk.PyBuffer[ImageType]
array = converter.GetArrayFromImage(image1)
volume = zeros((array.shape[0], array.shape[1], 1))
volume[:,:,0] = array
writeTiffStackRGB("o:/temp/rgb",
                  redVolume = volume,
                  greenVolume=None,
                  blueVolume=None)
