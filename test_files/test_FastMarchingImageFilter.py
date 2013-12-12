import itk

image_type = itk.Image[itk.F, 3]
output_type = itk.Image[itk.UC, 3]

file_name = 'O:\\images\\HPFcere_vol\\HPF_rotated_tif\\median_then_gaussian_filter.nrrd'
reader = itk.ImageFileReader[image_type].New()
writer = itk.ImageFileWriter[output_type].New()

writerTestCopy = itk.ImageFileWriter[output_type].New()


reader.SetFileName(file_name)
reader.Update()

#seeds = itk.FastMarchingFilterType.NodeContainer.New()

#seeds = itk.FastMarchingImageFilter[image_type, image_type].NodeContainer.New()
InternalPixelType = itk.F
Dimension = 3
NodeType = itk.LevelSetNode[InternalPixelType, Dimension]
NodeContainer = itk.VectorContainer[itk.UI, NodeType]
seeds = NodeContainer.New()

seedPosition = [10, 10, 10]

node = NodeType()
seedValue = 0.0

node.SetValue(seedValue)
node.SetIndex(seedPosition)
seeds.Initialize()
seeds.InsertElement(0, node)


#seeds = itk.FastMarchingImageFilter.NodeContainer.New()

fastMarching = itk.FastMarchingImageFilter[image_type, image_type].New()
fastMarching.SetTrialPoints(seeds)
fastMarching.SetInput(reader.GetOutput())
fastMarching.Update()

writer.SetFileName("o:\\temp\\fastmarching.nrrd")

writerTestCopy.SetFileName("o:\\temp\\test.nrrd")
#writerTestCopy.SetInput(reader)


caster = itk.RescaleIntensityImageFilter[image_type, output_type].New()
casterTest = itk.RescaleIntensityImageFilter[image_type, output_type].New()
#caster = itk.CastFilterType

casterTest.SetInput(reader.GetOutput())
writerTestCopy.SetInput(casterTest.GetOutput())
casterTest.SetOutputMinimum(0)
casterTest.SetOutputMaximum(255)

writerTestCopy.Update()

caster.SetInput(fastMarching.GetOutput())
writer.SetInput(caster.GetOutput())
caster.SetOutputMinimum(0)
caster.SetOutputMaximum(255)

writer.Update()

