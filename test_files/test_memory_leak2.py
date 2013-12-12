import itk, sys, gc
itk.auto_progress()
import numpy
#globalVolume = None

# image size is 1 GB
# IT = itk.Image.UC3
# img = IT.New(Regions=1000)

# image size is 1 GB
IT = itk.Image.F3
#img = IT.New(Regions=[1000, 1000, 250])
img = IT.New(Regions=[1000, 100, 250])

img.Allocate()
img.FillBuffer(0)
itk.write(img, "/tmp/result.nrrd")

print img

# exercise buffer conversion from itk to numpy
for i in range(1000):
 buf = itk.PyBuffer[IT].GetArrayFromImage(img)
 #buf = zeros((1000, 1000, 250))
del buf

# exercise buffer conversion from numpy to itk

count = 0

def callback():
 global count
 sys.stderr.write(str(count)+"\t")
 if count%10 == 0:
   sys.stderr.write("\n")
 sys.stderr.flush()
 count += 1
com = itk.PyCommand.New()
com.SetCommandCallable( callback )

buf = itk.PyBuffer[IT].GetArrayFromImage(img)
#buf = numpy.zeros((100, 100, 250))
buf[1, 2, 3] = 20
buf[:, :, :] = numpy.ones((250, 100, 1000))
#buf[:, :, :] = 1

def functionTest(volume):
    itk.write(volume, "/tmp/temp.nrrd")

def functionTest2(buf_test):
    #itk.write(volumeGlobal, "/tmp/temp.nrrd")
    if 1:
        bi = itk.PyBuffer[IT].GetImageFromArray(buf_test)
    itk.write(bi, "/tmp/temp2.nrrd")

for i in range(100000):
 global volumeGlobal
 print i
 print buf[1, 2, 3]
 print buf[1, 2, 4]
 bi = itk.PyBuffer[IT].GetImageFromArray(buf)
 itk.write(bi, "/tmp/result2.nrrd")
 #functionTest(bi)
 volumeGlobal = bi
 functionTest2(buf)
 #bi.AddObserver( itk.DeleteEvent(), com )
 ImageType = itk.Image[itk.F, 3]
 converter = itk.PyBuffer[ImageType]
 #buf2 = itk.PyBuffer[IT].GetArrayFromImage(bi)
 buf2 = converter.GetArrayFromImage(bi)
del bi

# force garbage collection
gc.collect()

sys.stderr.write(str(count)+"\n")

sys.exit(abs(1000-count))
