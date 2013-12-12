import itk
from numpy import *

def makeItkImage(dimensions, pixelType):
    Dimension = 2
    ImageType = itk.Image[pixelType, Dimension]
    
    index = itk.Index[2]()
    index.SetElement(0,0)
    index.SetElement(1,0)
    
    size = itk.Size[2]()
    size.SetElement(0, dimensions[0])
    size.SetElement(1, dimensions[1])
    
    imageRegion = itk.ImageRegion[2]()
    imageRegion.SetSize(size)
    imageRegion.SetIndex(index)
    
    
    image = ImageType.New()
    #image.SetSize([10,10])
    #image.SetIndex([0,0])
    #image.SetPixel([0,0], 0)
    
    image.SetRegions(imageRegion)
    image.Allocate()
    image.FillBuffer(0)
    
    return image


def printImageTest(image):
    #print image.GetImageDimension()
    region = image.GetLargestPossibleRegion()
    size = region.GetSize()
    print size.GetElement(0)
    print size.GetElement(1)

    image.FillBuffer(100)

    #index = itk.Index[2]()
    #index.SetElement(0, 5)
    #index.SetElement(1, 5)

    image.SetPixel([5,5], 10)
    image.SetPixel([5,6], 20)
    #image.SetPixel(index, 10)
    
    for i in range(size.GetElement(0)):
        for j in range(size.GetElement(1)):
            index = itk.Index[2]()
            index.SetElement(0, i)
            index.SetElement(1, j)
            #print i, j, ":", image.GetPixel(index)
            print i, j, ":", image.GetPixel([i,j])


def numpyToItk(numpyArray):

    itkImage = makeItkImage(numpyArray.shape, itk.F)

    index = [None, None]
    for i in range(numpyArray.shape[0]):
        for j in range(numpyArray.shape[1]):
            index[0] = i
            index[1] = j
            itkImage.SetPixel(index, numpyArray[i,j])

    return itkImage

    
def itkToNumpy(itkImage):

    region = itkImage.GetLargestPossibleRegion()
    size = region.GetSize()
    
    numpyArray = zeros((size.GetElement(0), size.GetElement(1)), dtype=float)

    index = [None, None]
    for i in range(size.GetElement(0)):
        for j in range(size.GetElement(1)):
            index[0] = i
            index[1] = j
            numpyArray[i,j] = itkImage.GetPixel(index)

    return numpyArray



    
#InternalPixelType = itk.F
#InternalPixelType = itk.UC
Dimension = 2
ImageType = itk.Image[itk.F, Dimension]
OutputImageType = itk.Image[itk.UC, Dimension]

#image = makeItkImage((10,20))
#printImageTest(image)

ReaderType = itk.ImageFileReader[ImageType]
WriterType = itk.ImageFileWriter[OutputImageType]

reader = ReaderType.New()
writer = WriterType.New()

reader.SetFileName("O:\\images\\3D-blob-data\\caulobacter0016.bmp")
reader.Update()
inputImage = reader.GetOutput()

array = itkToNumpy(inputImage)

modifiedArray = -array
minimum = modifiedArray.min()
modifiedArray = modifiedArray - minimum

outputImage = numpyToItk(modifiedArray)

CastFilterType = itk.RescaleIntensityImageFilter[ImageType, OutputImageType]
caster = CastFilterType.New()
caster.SetInput(outputImage)

writer.SetInput(caster.GetOutput())
writer.SetFileName("o:\\temp\\itk_numpy_test.bmp")
writer.Update()





