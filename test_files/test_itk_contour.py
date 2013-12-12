#/*=========================================================================
#
#  Program:   Insight Segmentation & Registration Toolkit
#  Module:    $RCSfile: SurfaceExtraction.cxx,v $
#  Language:  C++
#  Date:      $Date: 2005-08-27 01:46:04 $
#  Version:   $Revision: 1.3 $
#
#  Copyright (c) Insight Software Consortium. All rights reserved.
#  See ITKCopyright.txt or http://www.itk.org/HTML/Copyright.htm for details.
#
#     This software is distributed WITHOUT ANY WARRANTY; without even 
#     the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
#     PURPOSE.  See the above copyright notices for more information.
#
#=========================================================================*/

import itk

Dimension = 3
PixelType = itk.UC

ImageType = itk.Image[PixelType, Dimension]


ReaderType = itk.ImageFileReader[ImageType]
reader = ReaderType.New()
reader.SetFileName("O:\\images\\brainmaps\\000.jpg")

reader.Update()

TraitsType = itk.DefaultDynamicMeshTraits[itk.D, 2, 2, itk.D]

MeshType = itk.Mesh[itk.D, 2, TraitsType]

MeshSourceType = itk.BinaryMask3DMeshSource[ImageType, MeshType]

meshSource = MeshSourceType.New()

objectValue = 1

meshSource.SetObjectValue(objectValue)

meshSource.SetInput(reader.GetOutput())

meshSource.Update()

print "Nodes = ", meshSource.GetNumberOfNodes()
print "Cells = ", meshSource.GetNumberOfCells()






