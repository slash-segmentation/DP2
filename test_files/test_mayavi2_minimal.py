
import numpy

# Enthought library imports
from enthought.mayavi.scripts import mayavi2

#import enthought
from enthought.mayavi import mlab as enthought_mlab




def view_numpy():
    

    my_test_molecule()

    

def my_test_molecule():
    oxygen = enthought_mlab.points3d(1, 1, 1, scale_factor=16, scale_mode='none', resolution=20, color=(1,0,0), name='Oxygen')#    nitrogen = points3d(nx, ny, nz, scale_factor=20, scale_mode='none',


view_numpy()
