import itk
from sys import argv, stderr, exit

from numpy import *


IT = itk.Image.F3
inputVolume = IT.New(Regions=[1000, 100, 250])
inputVolume.Allocate()
inputVolume.FillBuffer(0)


#itk.auto_progress(2)

def fastMarch():

    
    
    seedPosition = (5, 5, 5)

    

      
    #itk.auto_progress(2)
    
    
    InternalImageType = IT
    
    
    
    
    FastMarchingFilterType = itk.FastMarchingUpwindGradientImageFilter[ InternalImageType, 
                                InternalImageType ]

    Dimension = 3
    NodeType = itk.LevelSetNode[itk.F, Dimension]
    NodeContainer = itk.VectorContainer[itk.UI, NodeType]

    
    stopPoints = NodeContainer.New()
    for i in range(5):
        stopPointNode = NodeType()
        stopPointNode.SetValue(0) #todo: is this needed
        stopPointNode.SetIndex([0, 0, 0])
        stopPoints.InsertElement(0, stopPointNode)
    
    fastMarching = FastMarchingFilterType.New()
    fastMarching.SetTargetReachedModeToOneTarget()
    fastMarching.SetTargetOffset(0)
    fastMarching.SetTargetPoints(stopPoints)

    fastMarching.SetInput(inputVolume)
    
    
    
    seeds = NodeContainer.New()
    
    
    
    node = NodeType()
    seedValue = 0.0
    
    node.SetValue( seedValue )
    node.SetIndex( seedPosition )
    
    seeds.Initialize();
    seeds.InsertElement( 0, node )
    
    fastMarching.SetTrialPoints(  seeds  );
    
    
    fastMarching.SetOutputSize(inputVolume.GetBufferedRegion().GetSize())
    
    stoppingTime = float( 1 )
    
    fastMarching.SetStoppingValue(  stoppingTime  )
    
    resultItkArray = fastMarching.GetOutput()
    fastMarching.Update()
    return None


for i in range(10000):
    print i
    fastMarch()

