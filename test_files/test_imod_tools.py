from imod_tools import *
import imod_tools

#import struct


def testInsertingPointsIntoTemplateFile():
    
    file = open('template.imod', "rb")
    str = file.read()
    file.close()
    
    
    
            
        
    readImodString(str)
    #print makeContourForSingleSphere()
    
    md = ModelData()
    md.readFromString(str[0:sizeOfModelDataStructure])
    print md.id
    print md.name
    print md.objsize
    print md.makeString()
    md.objsize = 1
    
    sz = chunkSize(str, sizeOfModelDataStructure)
    print ("size of object data %d" % sz)
    od = ObjectData()
    od.readFromString(str[sizeOfModelDataStructure:sizeOfModelDataStructure+sz])
    print "object contours"
    print od.contsize
    print od.id
    od.contsize = 5
    
    outFile = open('c:\\temp\\out.imod', 'wb')
    outFile.write(md.makeString())
    outFile.write(od.makeString())
    outFile.write(makeContourForSingleSphere([10,20,30], 5))
    outFile.write(makeContourForSingleSphere([10,30,30], 2.5))
    outFile.write(makeContourForSingleSphere([10,40,30], 5))
    outFile.write(makeContourForSingleSphere([10,25,30], 5))
    outFile.write(makeContourForSingleSphere([10,27,50], 5))
    #outFile.write('IEOF')
    outFile.write(imod_tools.restOfFile)
    outFile.close()
    
    
    #template = str[0:firstChunkLocation]
    
def testInsertingPointsIntoFile():
    
    f = open("O:\\images\\LFong\\tif_8bit_10_images\\test.cytoseg")
    doc = pickle.load(f)
    particles = doc.particleGroup.getAll()
    
    
    points = []
    for p in particles:
        points.append(p.loc)
        print p.loc
   
    #points = read points from file
    
    imod_tools.IMODFileInsertPoints("O:\\images\\LFong\\tif_8bit_10_images\\test.imod", "O:\\images\\LFong\\tif_8bit_10_images\\test_with_inserted_points.imod", points, doc.volumeShape, 9)
    #imod_tools.IMODFileInsertPoints("template.imod", "O:\\images\\LFong\\tif_8bit_10_images\\test_with_inserted_points.imod", points, 9)
    
    
#testInsertingPointsIntoTemplateFile()

testInsertingPointsIntoFile()

#file = open('template.imod', "rb")
#s = file.read()
#file.close()
#print readIMODString(s)


               
           
