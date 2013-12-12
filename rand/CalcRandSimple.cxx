
#include <vector>
#include <map>
#include <utility>

#include <ctime>

#include "util.h"

#include "itkImage.h"
#include "itkImageRegionIterator.h"
#include <itkBinaryThresholdImageFilter.h>
#include "itkInvertIntensityImageFilter.h"
#include "itkScalarConnectedComponentImageFilter.h"
#include "itkRelabelComponentImageFilter.h"
#include "itkImageFileReader.h"
#include "itkVTKImageIO.h"
#include "itkImageFileWriter.h"
#include "itkMedianImageFilter.h"
#include "itkImageRegionIterator.h"
#include "itkSimpleFilterWatcher.h"
#include "itkImageRegionIterator.h"
#include "itkMersenneTwisterRandomVariateGenerator.h"
#include "itkDiscreteGaussianImageFilter.h"
#include "itkWatershedImageFilter.h"
#include "itkUnaryFunctorImageFilter.h"
#include "itkCastImageFilter.h"
#include "itkScalarToRGBPixelFunctor.h"


const unsigned int    Dimension = 3;
//const unsigned short  PixelType;
typedef unsigned short LabelType;
typedef itk::Image< LabelType, Dimension>    LongImageType;
typedef itk::ImageRegionIterator< LongImageType > LongImageRegionIterator;
       
double calcRand( const LongImageType::Pointer& thresh_image,
                 const LongImageType::Pointer& train_pos );

double calcRandOpt( const LongImageType::Pointer& thresh_image,
                    const LongImageType::Pointer& train_pos );

int main(int argc, char* argv[] )
{
  if( argc < 3 )
    {
    std::cerr << "Missing Parameters " << std::endl;
    std::cerr << "Usage: " << argv[0];
    std::cerr << " train_pos_flood.mha ";
    std::cerr << " segment.mha" ;
    //std::cerr << " train_exclude.mha segment_float.mha" ;
    std::cerr << endl ;
    return 1;
    }

  char* train_pos_filename = argv[1];
  char* seg_float_filename = argv[2];

  bool blab = false;
  LongImageType::Pointer train_pos = load< LongImageType >( train_pos_filename, blab );
  LongImageType::Pointer seg_float = load< LongImageType >( seg_float_filename, blab );

  // slow rand calculation
//  double rand = calcRand( seg_float, train_pos );
//  printf( "%.03f\n", rand );

  // fast rand calculation
  double rand_opt = calcRandOpt( seg_float, train_pos );
  printf( "%.03f\n", rand_opt );

  return 0;
}

//
//  calcRand using simple computational form:
//  c(Y,Y') = [ (n choose 2 ) - 
//             ( 1/2 ( Sum_i(Sum_j nij)^2  +
//                     Sum_j(Sum_i nij)^2 ) -
//                   Sum(Sum nij^2) ] / ( n choose 2 )
//  where nij is the number of points in the ith cluster of Y and the ith
//  cluster of Y'
//  Runs in O(N)
//
double calcRandOpt( const LongImageType::Pointer& thresh_image,
             const LongImageType::Pointer& train_pos )
{
   double rand = 0;
   double N = 0;

   typedef pair< LabelType, LabelType > ijpair;
   map< ijpair, unsigned long > nij;
   map< ijpair, unsigned long >::iterator nij_iter;

   vector< LabelType > i_labels;
   vector< LabelType > j_labels;

   // make all the nij pairs
   LongImageRegionIterator thresh_i( thresh_image, 
         thresh_image->GetLargestPossibleRegion().GetSize() );
   LongImageRegionIterator train_j( train_pos, 
         train_pos->GetLargestPossibleRegion().GetSize() );
   thresh_i.GoToBegin();
   train_j.GoToBegin();
   while( !thresh_i.IsAtEnd() )
   {
      LabelType i_label = thresh_i.Get();
      LabelType j_label = train_j.Get();

      if( j_label != 0 )
      {
         ijpair ij( i_label, j_label );

         nij_iter = nij.find( ij );
         if ( nij_iter == nij.end() )
            nij[ ij ] = 1;
         else
            (*nij_iter).second = (*nij_iter).second++;

         // keep track of the labels for later
         vector< LabelType >::iterator liter = find( i_labels.begin(), i_labels.end(), i_label );
         if( liter == i_labels.end() )
            i_labels.push_back( i_label );
         liter = find( j_labels.begin(), j_labels.end(), j_label );
         if( liter == j_labels.end() )
            j_labels.push_back( j_label );

         ++N;
      }
      ++thresh_i;
      ++train_j;
   }
//   cout << "N: " << N << endl ;
//   cout << "map: " << endl;
//   for( nij_iter = nij.begin(); nij_iter != nij.end(); ++nij_iter )
//      cout << (nij_iter->first).first << ", " << nij_iter->first.second 
//           << ": " << nij_iter->second << endl ;

   // calculate Sum_i(Sum_j nij)^2
   double ij_sums = 0;
   for( unsigned int ii = 0; ii < i_labels.size(); ii++ )
   {
      double i_sums = 0;
      for( unsigned int jj = 0; jj < j_labels.size(); jj++ )
      {
         ijpair ij( i_labels[ii], j_labels[jj] );
         i_sums += nij[ ij ];
      }
      ij_sums += i_sums * i_sums; 
   }
   //cout << "ij_sums: " <<  ij_sums << endl;

   // calculate Sum_j(Sum_i nij)^2
   double ji_sums = 0;
   for( unsigned int jj = 0; jj < j_labels.size(); jj++ )
   {
      double j_sums = 0;
      for( unsigned int ii = 0; ii < i_labels.size(); ii++ )
      {
         ijpair ij( i_labels[ii], j_labels[jj] );
         j_sums += nij[ ij ];
      }
      ji_sums += j_sums * j_sums;
   }
   //cout << "ji_sums: " <<  ji_sums << endl;

   // calulate Sum(Sum nij^2 )
   double nij_square = 0;
   for( nij_iter = nij.begin(); nij_iter != nij.end(); ++nij_iter )
      nij_square += ( nij_iter->second * nij_iter->second );

   // (n choose 2 )
   double nchoose2 = ( (N*N) - N ) / 2.0;

   // put it all together
   rand = ( nchoose2 - 
         ( .5 * ( ij_sums + ji_sums ) - nij_square  ) ) 
              / nchoose2;

   return rand;
}


//
//  calcROC
//
double calcRand( const LongImageType::Pointer& thresh_image,
             const LongImageType::Pointer& train_pos )
{
   long int rand = 0;
   long int num_compares = 0;
   
   LongImageRegionIterator thresh_i( thresh_image, 
         thresh_image->GetLargestPossibleRegion().GetSize() );
   LongImageRegionIterator thresh_j( thresh_image, 
         thresh_image->GetLargestPossibleRegion().GetSize() );
   LongImageRegionIterator train( train_pos, 
         train_pos->GetLargestPossibleRegion().GetSize() );
   for( thresh_i.GoToBegin(); !thresh_i.IsAtEnd(); ++thresh_i )
   {
      long val_i = thresh_i.Get();
      //cout << thresh_i.GetIndex() << endl;

      thresh_j.SetIndex( thresh_i.GetIndex() );
      ++thresh_j; // skip the same index
      while( !thresh_j.IsAtEnd() )
      {
         long val_j = thresh_j.Get();

         long train_i = train_pos->GetPixel( thresh_i.GetIndex() );
         long train_j = train_pos->GetPixel( thresh_j.GetIndex() );

         //cout << thresh_i.GetIndex() << ": " 
         //   << val_i << ", " << val_j << " - " 
         //   << train_i << ", " << train_j << endl ;

         if( ( train_i != 0 ) && ( train_j != 0 ) ) // exclude membrane pixels
         {
            if( ( val_i == val_j ) && ( train_i == train_j ) )
               rand++;
            else if( ( val_i != val_j ) && ( train_i != train_j ) )
               rand++;

            ++num_compares;
         }
         ++thresh_j;
      }

   }

   double rand_val = (double)rand / (double)num_compares;

   return rand_val;
}

