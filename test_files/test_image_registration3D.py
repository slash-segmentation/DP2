#

import itk

from sys import argv

#
# Read the fixed and moving images using filenames
# from the command line arguments
#

ImageType = itk.Image[itk.F, 3]
ImageReaderType = itk.ImageFileReader[ImageType]

fixedImageReader = ImageReaderType.New()
movingImageReader = ImageReaderType.New()

fixedImageReader.SetFileName(  "data/A.nrrd" )
movingImageReader.SetFileName( "data/B.nrrd" )

fixedImageReader.Update()
movingImageReader.Update()

fixedImage = fixedImageReader.GetOutput() 
movingImage = movingImageReader.GetOutput()

#
#  Instantiate the classes for the registration framework
#

ImageRegistrationMethodType = itk.ImageRegistrationMethod[ImageType, ImageType]
MeanSquaresImageToImageMetricType = itk.MeanSquaresImageToImageMetric[ImageType, ImageType]
AffineTransformType = itk.AffineTransform[itk.D, 3]
LinearInterpolateImageFunctionType = itk.LinearInterpolateImageFunction[ImageType, itk.D]

registration    = ImageRegistrationMethodType.New()
imageMetric     = MeanSquaresImageToImageMetricType.New()
transform       = AffineTransformType.New()
optimizer       = itk.RegularStepGradientDescentOptimizer.New()
interpolator    = LinearInterpolateImageFunctionType.New()

registration.SetOptimizer(      optimizer.GetPointer() )
registration.SetTransform(      transform.GetPointer() )
registration.SetInterpolator(   interpolator.GetPointer() )
registration.SetMetric(         imageMetric.GetPointer() )
registration.SetFixedImage(  fixedImage )
registration.SetMovingImage( movingImage )
registration.SetFixedImageRegion(  fixedImage.GetBufferedRegion() )



TransformInitializerType = itk.CenteredTransformInitializer[
                                            AffineTransformType, 
                                            ImageType, 
                                            ImageType]

initializer = TransformInitializerType.New()
initializer.SetTransform(   transform )
initializer.SetFixedImage(  fixedImageReader.GetOutput() )
initializer.SetMovingImage( movingImageReader.GetOutput() )
initializer.MomentsOn()
initializer.InitializeTransform()



##
## Initial transform parameters 
##
#transform.SetAngle( 0.0 );
#
## center of the fixed image
#fixedSpacing = fixedImage.GetSpacing()
#fixedOrigin = fixedImage.GetOrigin()
#fixedSize = fixedImage.GetLargestPossibleRegion().GetSize()
#
#centerFixed = ( fixedOrigin.GetElement(0) + fixedSpacing.GetElement(0) * fixedSize.GetElement(0) / 2.0,
#                fixedOrigin.GetElement(1) + fixedSpacing.GetElement(1) * fixedSize.GetElement(1) / 2.0 )
#
## center of the moving image 
#movingSpacing = movingImage.GetSpacing()
#movingOrigin = movingImage.GetOrigin()
#movingSize = movingImage.GetLargestPossibleRegion().GetSize()
#
#centerMoving = ( movingOrigin.GetElement(0) + movingSpacing.GetElement(0) * movingSize.GetElement(0) / 2.0,
#                 movingOrigin.GetElement(1) + movingSpacing.GetElement(1) * movingSize.GetElement(1) / 2.0  )
#
## transform center
#center = transform.GetCenter()
#center.SetElement( 0, centerFixed[0] )
#center.SetElement( 1, centerFixed[1] )
#
## transform translation
#translation = transform.GetTranslation()
#translation.SetElement( 0, centerMoving[0] - centerFixed[0] )
#translation.SetElement( 1, centerMoving[1] - centerFixed[1] )

initialParameters = transform.GetParameters()

print "Initial Parameters: "
#print "Angle: %f" % (initialParameters.GetElement(0), )
#print "Center: %f, %f" % ( initialParameters.GetElement(1), initialParameters.GetElement(2) )
#print "Translation: %f, %f" % (initialParameters.GetElement(3), initialParameters.GetElement(4))

registration.SetInitialTransformParameters( initialParameters )

#
# Define optimizer parameters
#

# optimizer scale
translationScale = 1.0 / 1000.0

ArrayType = itk.Array[itk.D]
optimizerScales = ArrayType( transform.GetNumberOfParameters() )
optimizerScales.SetElement(0, 1.0)
optimizerScales.SetElement(1, 1.0)
optimizerScales.SetElement(2, 1.0)
optimizerScales.SetElement(3, 1.0)
optimizerScales.SetElement(4, 1.0)
optimizerScales.SetElement(5, 1.0)
optimizerScales.SetElement(6, 1.0)
optimizerScales.SetElement(7, 1.0)
optimizerScales.SetElement(8, 1.0)
optimizerScales.SetElement(9, translationScale)
optimizerScales.SetElement(10, translationScale)
optimizerScales.SetElement(11, translationScale)


optimizer.SetScales( optimizerScales )
optimizer.SetMaximumStepLength( 0.1 )
optimizer.SetMinimumStepLength( 0.001 )
optimizer.SetNumberOfIterations( 200 )

#
# Iteration Observer
#
def iterationUpdate():
    currentParameter = transform.GetParameters()
    #print "M: %f   P: %f %f %f %f %f " % ( optimizer.GetValue(),
    #                             currentParameter.GetElement(0),
    #                             currentParameter.GetElement(1),
    #                             currentParameter.GetElement(2),
    #                             currentParameter.GetElement(3),
    #                             currentParameter.GetElement(4) )
    print "optimizer.GetValue(): %f" % optimizer.GetValue()

 
iterationCommand = itk.PyCommand.New()
iterationCommand.SetCommandCallable( iterationUpdate )
optimizer.AddObserver( itk.IterationEvent(), iterationCommand.GetPointer() )

print "Starting registration"

#
# Start the registration process
#

registration.StartRegistration()

#
# Get the final parameters of the transformation
#
finalParameters = registration.GetLastTransformParameters()

print "Final Registration Parameters "
#print "Angle in radians  = %f" % finalParameters.GetElement(0)
#print "Rotation Center X = %f" % finalParameters.GetElement(1)
#print "Rotation Center Y = %f" % finalParameters.GetElement(2)
#print "Translation in  X = %f" % finalParameters.GetElement(3)
#print "Translation in  Y = %f" % finalParameters.GetElement(4)

# Now, we use the final transform for resampling the moving image.
ResampleImageFilterType = itk.ResampleImageFilter[ImageType, ImageType]
resampler = ResampleImageFilterType.New()

resampler.SetTransform( transform.GetPointer() )
resampler.SetInput( movingImage )

region = fixedImage.GetLargestPossibleRegion()

resampler.SetSize( region.GetSize() )
resampler.SetOutputSpacing( fixedImage.GetSpacing() )
resampler.SetOutputDirection( fixedImage.GetDirection() )
resampler.SetOutputOrigin(  fixedImage.GetOrigin() )
resampler.SetDefaultPixelValue( 100 )

#
# Cast for output
#
USImageType = itk.Image[itk.US, 3]
RescaleIntensityImageFilterType = itk.RescaleIntensityImageFilter[ImageType, USImageType]
outputCast = RescaleIntensityImageFilterType.New()
outputCast.SetInput( resampler.GetOutput() )
outputCast.SetOutputMinimum( 0 )
outputCast.SetOutputMaximum( 65535 )
ImageFileWriterType = itk.ImageFileWriter[USImageType]
writer = ImageFileWriterType.New()

writer.SetFileName( "c:/temp/out.nrrd" )
writer.SetInput( outputCast.GetOutput() )
writer.Update()

print "file written"




