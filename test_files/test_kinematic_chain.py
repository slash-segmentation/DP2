from enthought.tvtk.api import tvtk
from math import *
from numpy import *
from geometry import *



zDirection = array((0, 0, 1))



class Pipe:

    def __init__(self):
        self.points = []
        self.pipeRibs = {}
        self.spokeEndPointIndexDict = None
        self.allSpokeEndPoints = None
    
    def addRib(self, spokeLengths):
        count = len(self.pipeRibs)
        self.pipeRibs[count] = PipeRib(self, spokeLengths)
        
    def spokeEndPointBeforeFinalTransform(self, ribIndex, spokeIndex):
        pipeRib = self.pipeRibs[ribIndex]
        angleStep = 2 * pi / len(pipeRib.spokeLengths)
        angle = angleStep * spokeIndex
        length = pipeRib.spokeLengths[spokeIndex]
        position = length * array((cos(angle), sin(angle)))
        return array((position[0], position[1], 0))
    
    def ribOriginPoint(self, ribIndex):
        p1 = array(pipe.points[ribIndex])
        p2 = array(pipe.points[ribIndex+1])
        return centerPoint(p1, p2)
    
    def makeSpokeActor(self, ribIndex, spokeIndex):
        spoke = tvtk.LineSource(
                    point1=array((0, 0, 0)),
                    point2=self.spokeEndPointBeforeFinalTransform(ribIndex, spokeIndex))
        spokeTransformFilter = tvtk.TransformFilter(input=spoke.output)
        spokeTransform = tvtk.Transform()
        spokeTransform.translate(self.ribOriginPoint(ribIndex))
        #spokeTransform.rotate_wxyz(degrees(rotationAngle), axis[0], axis[1], axis[2])
        spokeTransform.concatenate(self.boneRotationTransform(ribIndex))
        spokeTransformFilter.transform = spokeTransform
        spokeMapper = tvtk.PolyDataMapper(input=spokeTransformFilter.output)
        spokeActor = tvtk.Actor(mapper=spokeMapper)
        return spokeActor


    def boneDirection(self, ribIndex):
        p1 = array(pipe.points[ribIndex])
        p2 = array(pipe.points[ribIndex+1])
        return unitVectorFromPoints(p1, p2)


    def boneRotationTransform(self, ribIndex):
        transform = tvtk.Transform()
        rotationAngle = acos(vdot(zDirection, self.boneDirection(ribIndex)))
        axis = cross(zDirection, self.boneDirection(ribIndex))
        transform.rotate_wxyz(degrees(rotationAngle), axis[0], axis[1], axis[2])
        return transform


    def spokeEndPoint(self, ribIndex, spokeIndex):
        transform = tvtk.Transform()
        #spokeEndPoint = array((position[0], position[1], 0))
        point = pipe.spokeEndPointBeforeFinalTransform(ribIndex, spokeIndex)
        #print "rotationAngle", rotationAngle, "axis", axis
        transform.translate(self.ribOriginPoint(ribIndex))
        #transform.rotate_wxyz(degrees(rotationAngle), axis[0], axis[1], axis[2])
        transform.concatenate(self.boneRotationTransform(ribIndex))
        transform.translate(point)
        return transform.position


    def makeEndOfSpokeMarkerActor(self, ribIndex, spokeIndex):
        # create end of spoke marker
        transform = tvtk.Transform()
        sphere = tvtk.SphereSource(theta_resolution=12, phi_resolution=12)
        transform.translate(self.spokeEndPoint(ribIndex, spokeIndex))
        transform.scale((0.2, 0.2, 0.2))
        transformFilter = tvtk.TransformFilter(input=sphere.output)
        transformFilter.transform = transform
        mapper = tvtk.PolyDataMapper(input=transformFilter.output)
        actor = tvtk.Actor(mapper=mapper)
        return actor


    def updateAllSpokeEndPoints(self):
        
        self.spokeEndPointIndexDict = {}
        self.allSpokeEndPoints = []
        count = 0
        for ribIndex in range(len(self.pipeRibs)):
            pipeRib = self.pipeRibs[ribIndex]
            for spokeIndex in range(len(pipeRib.spokeLengths)):
                self.allSpokeEndPoints.append(self.spokeEndPoint(ribIndex, spokeIndex))
                self.spokeEndPointIndexDict[(ribIndex, spokeIndex)] = count
                count += 1


    def getSpokeEndPointIndex(self, ribIndex, spokeIndex):
        if self.spokeEndPointIndexDict == None:
            raise Exception, "Spoke end points not initialized. Use updateAllSpokeEndPoints to initialize the points list."
        else:
            return self.spokeEndPointIndexDict[(ribIndex, spokeIndex)]



class PipeRib:

    def __init__(self, parentPipe, spokeLengths):
        self.parentPipe = parentPipe
        self.spokeLengths = spokeLengths
        


pipe = Pipe()
pipe.points.append((0, 0, 0))
pipe.points.append((0, 0, 4))
pipe.points.append((1, 1, 8))
pipe.points.append((1, 0, 14))
pipe.addRib([2, 2, 2])
pipe.addRib([2, 2, 3])
pipe.addRib([2, 2, 2])


if 0:
    #sphereSource = tvtk.SphereSource(theta_resolution=12, phi_resolution=12)
    cs1 = tvtk.ConeSource(resolution=100)
    transform1 = tvtk.Transform()
    transform1.rotate_y(20)
    transform1.translate((5, 0, 0))
    cs2 = tvtk.ConeSource(resolution=100)
    transform2 = tvtk.Transform()
    
    tf1 = tvtk.TransformFilter(input=cs1.output)
    tf2 = tvtk.TransformFilter(input=cs1.output)
    tf1.transform = transform1
    tf2.transform = transform2
    
    mapper1 = tvtk.PolyDataMapper(input=tf1.output)
    mapper2 = tvtk.PolyDataMapper(input=tf2.output)





if 0:
    cs = tvtk.ConeSource(resolution=100)
    mapper = tvtk.PolyDataMapper(input=cs.output)
    actor = tvtk.Actor(mapper=mapper)
    #actor1 = tvtk.Actor(mapper=mapper1)
    #actor2 = tvtk.Actor(mapper=mapper2)

# create a renderer:
renderer = tvtk.Renderer()
# create a render window and hand it the renderer:
render_window = tvtk.RenderWindow(size=(400,400))
render_window.add_renderer(renderer)

# create interactor and hand it the render window
# This handles mouse interaction with window.
interactor = tvtk.RenderWindowInteractor(render_window=render_window)
#renderer.add_actor(actor)
#renderer.add_actor(actor1)
#renderer.add_actor(actor2)


print "rendering"

def renderPipe():

    quads = []
    pipe.updateAllSpokeEndPoints()

    for i in range(len(pipe.points)):
        point = pipe.points[i]
        
        sphere = tvtk.SphereSource(theta_resolution=12, phi_resolution=12)
        transform = tvtk.Transform()
        transform.translate(point)
        transformFilter = tvtk.TransformFilter(input=sphere.output)
        transformFilter.transform = transform
        mapper = tvtk.PolyDataMapper(input=transformFilter.output)
        actor = tvtk.Actor(mapper=mapper)
        renderer.add_actor(actor)
    
        if i < (len(pipe.points) - 1):
    
            pipeRib = pipe.pipeRibs[i]
            p1 = array(pipe.points[i])
            p2 = array(pipe.points[i+1])
    
            bone = tvtk.LineSource(point1=p1, point2=p2)
            mapper = tvtk.PolyDataMapper(input=bone.output)
            actor = tvtk.Actor(mapper=mapper)
            renderer.add_actor(actor)
            
            #angleStep = 2 * pi / len(pipeRib.spokeLengths)
            #boneCenter = centerPoint(p1, p2)
            boneCenter = pipe.ribOriginPoint(i)
            
            for spokeIndex in range(len(pipeRib.spokeLengths)):
                #angle = angleStep * spokeIndex
                #length = pipeRib.spokeLengths[spokeIndex]
                #position = length * array((cos(angle), sin(angle)))
        
                endOfSpokeMarkerActor = pipe.makeEndOfSpokeMarkerActor(i, spokeIndex)
                renderer.add_actor(endOfSpokeMarkerActor)
    
                spokeActor = pipe.makeSpokeActor(i, spokeIndex)
                renderer.add_actor(spokeActor)
            
        if i < (len(pipe.points) - 2):

            for spokeIndex in range(len(pipeRib.spokeLengths)):
    
                if spokeIndex == len(pipeRib.spokeLengths) - 1:
                    nextSpokeIndex = 0
                else:
                    nextSpokeIndex = spokeIndex + 1
    
                print "i", i, "(len(pipe.points) - 1)", (len(pipe.points) - 1)
                pointIndex0 = pipe.getSpokeEndPointIndex(i, spokeIndex)
                pointIndex1 = pipe.getSpokeEndPointIndex(i, nextSpokeIndex)
                pointIndex2 = pipe.getSpokeEndPointIndex(i+1, nextSpokeIndex)
                pointIndex3 = pipe.getSpokeEndPointIndex(i+1, spokeIndex)
                #point1 = [point1[0], point1[1], point1[2]]
                #point2 = [0, 1, 0]
                #point3 = [1, 1, 0]
                #point4 = [1, 0, 0]
    
                #points = array([point1, point2, point3, point4], 'f')
                #quads = array([[0, 1, 2, 3]])
                quads.append([pointIndex0, pointIndex1, pointIndex2, pointIndex3])
                #print points
                #points = array([[0,0,0], [0,1,0], [1,1,0], [1,0,0], [0,0,1], [0,1,1]], 'f')
                #quads = array([[0,1,2,3], [0,4,5,1]])
                #points, temperature = data[:,:3], data[:,-1]
                #mesh = tvtk.PolyData(points=points, polys=quads)
                #mesh.point_data.scalars = temperature
                #triangleFilter = tvtk.TriangleFilter(input=mesh)
                #butterflyFilter = tvtk.ButterflySubdivisionFilter(input=triangleFilter.output,
                #                                                  number_of_subdivisions=5)
                
    pipe.updateAllSpokeEndPoints()
    mesh = tvtk.PolyData(points=pipe.allSpokeEndPoints, polys=quads)
    #mapper = tvtk.PolyDataMapper(input=butterflyFilter.output)
    triangleFilter = tvtk.TriangleFilter(input=mesh)
    butterflyFilter = tvtk.ButterflySubdivisionFilter(input=triangleFilter.output,
                                      number_of_subdivisions=5)
    #butterflyFilter = tvtk.ButterflySubdivisionFilter(input=mesh,
    #                                  number_of_subdivisions=5)

    #mapper = tvtk.PolyDataMapper(input=mesh)
    mapper = tvtk.PolyDataMapper(input=butterflyFilter.output)
    actor = tvtk.Actor(mapper=mapper)
    renderer.add_actor(actor)


renderPipe()
interactor.initialize()
interactor.start()
