#ifndef _track_util_h_
#define _track_util_h_

#include "itkRGBPixel.h"
#include "itkImageFileWriter.h"
#include "itkImageFileReader.h"
#include "itkImageRegionConstIteratorWithIndex.h"
#include "itkImageRegionIterator.h"
#include "itkNumericTraits.h"
#include "itkImageDuplicator.h"
#include "itkCastImageFilter.h"
#include "itkRescaleIntensityImageFilter.h"
#include "itkRescaleIntensityImageFilter.h"
#include "itkImage.h"

#include <vector>

using namespace std;

/*
template <typename image_t>
typename image_t::Pointer
extractImage(const image_t *img, 
      const image_t::IndexType start, const image_t::SizeType size)
{
   image_t::RegionType region;
   region.SetSize(size);
   region.SetIndex(start);

   typedef itk::RegionOfInterestImageFilter
      <>
   return 
}
*/

//----------------------------------------------------------------
// image_min_max
//
// Find min/max pixel values, return mean pixel value (average):
//
template <typename image_t>
double
image_min_max(const image_t * a,
      typename image_t::PixelType & min,
      typename image_t::PixelType & max)
{
   typedef typename image_t::PixelType pixel_t;
   typedef typename itk::ImageRegionConstIteratorWithIndex<image_t> iter_t;

   min = std::numeric_limits<pixel_t>::max();
   max = -min;

   double mean = 0.0;
   double counter = 0.0;
   iter_t iter(a, a->GetLargestPossibleRegion());
   for (iter.GoToBegin(); !iter.IsAtEnd(); ++iter)
   {
      pixel_t v = iter.Get();
      min = std::min(min, v);
      max = std::max(max, v);

      mean += double(v);
      counter += 1.0;
   }

   mean /= counter;
   return mean;
}

//----------------------------------------------------------------
// remap_min_max_inplace
// 
template <class image_t>
bool
remap_min_max_inplace(image_t * a,
		      typename image_t::PixelType new_min = 0,
		      typename image_t::PixelType new_max = 255)
{
  
  typedef typename image_t::PixelType pixel_t;
  typedef typename itk::ImageRegionIterator<image_t> iter_t;
  
  double min = std::numeric_limits<pixel_t>::max();
  double max = -min;
  
  iter_t iter(a, a->GetLargestPossibleRegion());
  for (iter.GoToBegin(); !iter.IsAtEnd(); ++iter)
  {
    double v = iter.Get();
    min = std::min(min, v);
    max = std::max(max, v);
  }
  
  double rng = max - min;
  if (rng == 0.0) return false;
  
  // rescale the intensities:
  double new_rng = new_max - new_min;
  for (iter.GoToBegin(); !iter.IsAtEnd(); ++iter)
  {
    double t = (iter.Get() - min) / rng;
    //cout<< "pretest: " << iter.Get() << endl;
    iter.
      Set(pixel_t(std::min(double(itk::NumericTraits<pixel_t>::max()),
			   std::max(double(itk::NumericTraits<pixel_t>::min()),
				    new_min + t * new_rng))));
    //cout << "test: " << pixel_t(std::min(double(itk::NumericTraits<pixel_t>::max()), std::max(double(itk::NumericTraits<pixel_t>::min()), new_min + t * new_rng))) << endl ;
  }
  
  return true;
}

//
//  new
//

template <class image_t>
typename image_t::Pointer
new2d(const int x, const int y )
{
   //typedef typename image_t image_tt;
   typename image_t::Pointer image = image_t::New();
   //image_t::Pointer image = image_t::New();
   typename image_t::IndexType start;
   start[ 0 ] = 0; start[ 1 ] = 0;
   typename image_t::SizeType size;
   size[ 0 ] = x; size[ 1 ] = y;
   typename image_t::RegionType region;
   region.SetSize( size );
   region.SetIndex( start );
   image->SetRegions( region );
   image->Allocate();
   image->FillBuffer( 0.0 );
   return image;
}

template <class image_t>
typename image_t::Pointer
new3d(const int x, const int y, const int z )
{
   //typedef typename image_t image_tt;
   typename image_t::Pointer image = image_t::New();
   //image_t::Pointer image = image_t::New();
   typename image_t::IndexType start;
   start[ 0 ] = 0; start[ 1 ] = 0; start[ 2 ] = 0;
   typename image_t::SizeType size;
   size[ 0 ] = x; size[ 1 ] = y; size[ 2 ] = z;
   typename image_t::RegionType region;
   region.SetSize( size );
   region.SetIndex( start );
   image->SetRegions( region );
   image->Allocate();
   image->FillBuffer( 0.0 );
   return image;
}


//
//  copy
//
template <class image_t>
typename image_t::Pointer
copy(const image_t* image)
{
   typedef typename itk::ImageDuplicator<image_t> dup_t;
   typename dup_t::Pointer duplicator = dup_t::New();
   duplicator->SetInputImage(image);
   duplicator->Update();
   return duplicator->GetOutput();
}

//
// load
//
template <class image_t>
typename image_t::Pointer
load(const char * filename, bool blab = true)
{
   typedef typename itk::ImageFileReader<image_t> reader_t;
   typename reader_t::Pointer reader = reader_t::New();
   reader->SetFileName(filename);

   if (blab) cout << "loading " << filename << endl;
   try
   {
      reader->Update();
   }
   catch (itk::ExceptionObject &ex)
   {
      std::cout << "------ Caught expected exception!" << std::endl;
      std::cout << ex;
      exit(1);
   }

   return reader->GetOutput();
}

//
// save
//
template <class image_t>
void
save(const image_t * image, const char * filename, bool blab = true)
{
      typedef typename itk::ImageFileWriter<image_t> writer_t;
      typename writer_t::Pointer writer = writer_t::New();
      writer->SetInput(image);

      if (blab) cout << "saving " << filename << endl;
      writer->SetFileName(filename);
      writer->Update();
      if ( !writer->GetImageIO()->CanReadFile(filename) )
      {
         cout << " ------------ CANNOT READ " << filename << endl ;
         exit(1);
         //return EXIT_FAILURE;
      }
}

//
// rescale
//
template <class image_t>
typename image_t::Pointer
rescale(image_t * image, float min, float max)
{
   typedef typename itk::RescaleIntensityImageFilter
      <image_t, image_t> RescaleFilterType;
   typename RescaleFilterType::Pointer intensityRescaler =
      RescaleFilterType::New();
   intensityRescaler->SetInput(image);
   intensityRescaler->SetOutputMinimum(min);
   intensityRescaler->SetOutputMaximum(max);
   intensityRescaler->Update();
   return intensityRescaler->GetOutput();
}

//
// save
//
template <class image_t>
void
save_as_png(const image_t * image, const char * filename, bool blab = true)
{
   typedef itk::RescaleIntensityImageFilter
                        <image_t, itk::Image<unsigned char,2> > caster;
   typename caster::Pointer cast = caster::New();
   cast->SetOutputMinimum(0);
   cast->SetOutputMaximum(255);
   cast->SetInput(image);
   cast->Update();

   itk::Image<unsigned char,2>::Pointer new_image = cast->GetOutput();
   typedef typename itk::ImageFileWriter<itk::Image<unsigned char,2> > writer_t;
   typename writer_t::Pointer writer = writer_t::New();
   writer->SetInput(cast->GetOutput());

   if (blab) cout << "saving " << filename << endl;
   writer->SetFileName(filename);
   writer->Update();
   if ( !writer->GetImageIO()->CanReadFile(filename) )
   {
      cout << " ------------ CANNOT READ " << filename << endl ;
      exit(1);
      //return EXIT_FAILURE;
   }

}

//
// save
//
template <class image_t>
void
save_as_tif(const image_t * image, const char * filename, bool blab = true)
{
   typedef itk::RescaleIntensityImageFilter
                        <image_t, itk::Image<unsigned short,2> > caster;
   typename caster::Pointer cast = caster::New();
   cast->SetOutputMinimum(0);
   cast->SetOutputMaximum( numeric_limits<unsigned short>::max( ) );
   cast->SetInput(image);
   cast->Update();

   itk::Image<unsigned short,2>::Pointer new_image = cast->GetOutput();
   typedef typename itk::ImageFileWriter<itk::Image<unsigned short,2> > writer_t;
   typename writer_t::Pointer writer = writer_t::New();
   writer->SetInput(cast->GetOutput());

   if (blab) cout << "saving " << filename << endl;
   writer->SetFileName(filename);
   writer->Update();
   if ( !writer->GetImageIO()->CanReadFile(filename) )
   {
      cout << " ------------ CANNOT READ " << filename << endl ;
      exit(1);
      //return EXIT_FAILURE;
   }

}

//
// 
//
template <class image_t>
typename itk::Image<unsigned char, 2>::Pointer
convert_to_char(const image_t * image)
{
   typedef itk::RescaleIntensityImageFilter
                        <image_t, itk::Image<unsigned char,2> > caster;
   typename caster::Pointer cast = caster::New();
   cast->SetOutputMinimum(0);
   cast->SetOutputMaximum(255);
   cast->SetInput(image);
   cast->Update();

   return cast->GetOutput();
}

//
// 
//
template <class image_t>
typename itk::Image< itk::RGBPixel< unsigned char >, 2>::Pointer
convert_to_rgb(const image_t * image)
{
   typedef itk::RescaleIntensityImageFilter
            <image_t, itk::Image< itk::RGBPixel< unsigned char >,2> > caster;
   typename caster::Pointer cast = caster::New();
   //cast->SetOutputMinimum(0);
   //cast->SetOutputMaximum(255);
   cast->SetInput(image);
   cast->Update();

   return cast->GetOutput();
}

#endif
