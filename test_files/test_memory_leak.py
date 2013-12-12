import itk
import numpy
import gc

ImageType = itk.Image[itk.F, 3]
converter = itk.PyBuffer[ImageType]

#inputNumpyVolume = numpy.ones((100, 100, 200))
#inputVolume = converter.GetImageFromArray(inputNumpyVolume)

inputVolume = {}
for i in range(10000):

    print i

    inputNumpyVolume = numpy.ones((100, 100, 200))
    inputVolume[i] = converter.GetImageFromArray(inputNumpyVolume)
    #inputVolume.__del__()
    #inputVolume.Delete()
    
    #array = converter.GetArrayFromImage(inputVolume)
    #print gc.get_objects()
    #print array[0, 0, 0]
    
    #inputVolume[i].__del__()
    #array.__del__()
    #gc.collect()
    inputVolume[i].Delete()
    inputVolume[i] = None

