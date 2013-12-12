from numpy import *
#import tvtk
from enthought.tvtk.api import tvtk

# create a renderer:
renderer = tvtk.Renderer()
# create a render window and hand it the renderer:
render_window = tvtk.RenderWindow(size=(400,400))
render_window.add_renderer(renderer)

# create interactor and hand it the render window
# This handles mouse interaction with window.
interactor = tvtk.RenderWindowInteractor(render_window=render_window)

#data = array([[0,0,0,10], [1,0,0,20],
#                      [0,1,0,20], [0,0,1,30]], 'f')
data = array([[0,0,0], [0,1,0], [1,1,0], [1,0,0], [0,0,1], [0,1,1]], 'f')
quads = array([[0,1,2,3], [0,4,5,1]])
#points, temperature = data[:,:3], data[:,-1]
#mesh = tvtk.PolyData(points=points, polys=quads)
mesh = tvtk.PolyData(points=data, polys=quads)
#mesh.point_data.scalars = temperature
triangleFilter = tvtk.TriangleFilter(input=mesh)
butterflyFilter = tvtk.ButterflySubdivisionFilter(input=triangleFilter.output,
                                                  number_of_subdivisions=5)

mapper = tvtk.PolyDataMapper(input=butterflyFilter.output)
actor = tvtk.Actor(mapper=mapper)
renderer.add_actor(actor)

interactor.initialize()
interactor.start()
