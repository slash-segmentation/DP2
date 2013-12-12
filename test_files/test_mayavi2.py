#!/usr/bin/env python

"""This script demonstrates how to create a numpy array data and
visualize it as image data using a few modules.

"""
# Author: Prabhu Ramachandran <prabhu_r@users.sf.net>
# Copyright (c) 2005-2008, Enthought, Inc.
# License: BSD Style.

# Standard library imports
import numpy

# Enthought library imports
from enthought.mayavi.scripts import mayavi2
from enthought.mayavi.sources.array_source import ArraySource
from enthought.mayavi.modules.outline import Outline
from enthought.mayavi.modules.image_plane_widget import ImagePlaneWidget

#import enthought
from enthought.mayavi import mlab as enthought_mlab

def make_data(dims=(12, 12, 12)):
    """Creates some simple array data of the given dimensions to test
    with."""
    np = dims[0]*dims[1]*dims[2]

    # Create some scalars to render.
    x, y, z = numpy.ogrid[-5:5:dims[0]*1j,-5:5:dims[1]*1j,-5:5:dims[2]*1j]
    x = x.astype('f')
    y = y.astype('f')
    z = z.astype('f')

    scalars = (numpy.sin(x*y*z)/(x*y*z))
    # The copy makes the data contiguous and the transpose makes it
    # suitable for display via tvtk.  Please note that we assume here
    # that the ArraySource is configured to not transpose the data.
    s = numpy.transpose(scalars).copy()
    # Reshaping the array is needed since the transpose messes up the
    # dimensions of the data.  The scalars themselves are ravel'd and
    # used internally by VTK so the dimension does not matter for the
    # scalars.
    s.shape = s.shape[::-1]
    
    return s


@mayavi2.standalone
def view_numpy():
    
    if 0:
    
        """Example showing how to view a 3D numpy array in mayavi2.
        """
        # 'mayavi' is always defined on the interpreter.
        mayavi.new_scene()
        #print mayavi.new_scene()
        print mayavi.new_scene.__doc__
        print type(mayavi)
        print type(mayavi.get_active_window())
        # Make the data and add it to the pipeline.
        data = make_data()
        src = ArraySource(transpose_input_array=False)
        src.scalar_data = data    
        mayavi.add_source(src)
        # Visualize the data.
        o = Outline()
        mayavi.add_module(o)
        ipw = ImagePlaneWidget()
        mayavi.add_module(ipw)
        ipw.module_manager.scalar_lut_manager.show_scalar_bar = True
    
        ipw_y = ImagePlaneWidget()
        mayavi.add_module(ipw_y)
        ipw_y.ipw.plane_orientation = 'y_axes'




#    # Create the data.
#    from numpy import pi, sin, cos, mgrid
#    dphi, dtheta = pi/250.0, pi/250.0
#    [phi,theta] = mgrid[0:pi+dphi*1.5:dphi,0:2*pi+dtheta*1.5:dtheta]
#    m0 = 4; m1 = 3; m2 = 2; m3 = 3; m4 = 6; m5 = 2; m6 = 6; m7 = 4;
#    r = sin(m0*phi)**m1 + cos(m2*phi)**m3 + sin(m4*theta)**m5 + cos(m6*theta)**m7
#    x = r*sin(phi)*cos(theta)
#    y = r*cos(phi)
#    z = r*sin(phi)*sin(theta)
#    
#    # View it.
#    from enthought.mayavi import mlab
#    s = mlab.mesh(x, y, z)
#    #mlab.show()





    my_test_molecule()

    

def my_test_molecule():
    """Generates and shows a Caffeine molecule."""
    o = [[30, 62, 19],[8, 21, 10]]
    ox, oy, oz = map(numpy.array, zip(*o))
    n = [[31, 21, 11], [18, 42, 14], [55, 46, 17], [56, 25, 13]]
    nx, ny, nz = map(numpy.array, zip(*n))
    c = [[5, 49, 15], [30, 50, 16], [42, 42, 15], [43, 29, 13], [18, 28, 12],
         [32, 6, 8], [63, 36, 15], [59, 60, 20]]
    cx, cy, cz = map(numpy.array, zip(*c))
    h = [[23, 5, 7], [32, 0, 16], [37, 5, 0], [73, 36, 16], [69, 60, 20],
         [54, 62, 28], [57, 66, 12], [6, 59, 16], [1, 44, 22], [0, 49, 6]]
    hx, hy, hz = map(numpy.array, zip(*h))

    #oxygen = enthought.mayavi.mlab.points3d(ox, oy, oz, scale_factor=16, scale_mode='none', resolution=20, color=(1,0,0), name='Oxygen')
    oxygen = enthought_mlab.points3d(1, 1, 1, scale_factor=16, scale_mode='none', resolution=20, color=(1,0,0), name='Oxygen')#    nitrogen = points3d(nx, ny, nz, scale_factor=20, scale_mode='none',
#                                resolution=20, color=(0,0,1), name='Nitrogen')
#    carbon = points3d(cx, cy, cz, scale_factor=20, scale_mode='none',
#                                resolution=20, color=(0,1,0), name='Carbon')
#    hydrogen = points3d(hx, hy, hz, scale_factor=10, scale_mode='none',
#                                resolution=20, color=(1,1,1), name='Hydrogen')
#
#    return oxygen, nitrogen, carbon, hydrogen
    #pass


if __name__ == '__main__':
    view_numpy()
