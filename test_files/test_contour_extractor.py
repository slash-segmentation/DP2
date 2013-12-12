import itk

ImageType = itk.Image[itk.F, 2]
ReaderType = itk.ImageFileReader[ImageType]

reader = ReaderType.New(FileName = "data/A.tiff")
image = reader.GetOutput()

ExtractorType = itk.ContourExtractor2DImageFilter[ImageType]

extractor = ExtractorType.New()
extractor.SetInput(image)
extractor.SetContourValue(100.0)
extractor.Update()
print extractor.GetNumberOfOutputs()
print extractor.GetOutputs()
print extractor.GetOutputs()[0].GetVertexList()
