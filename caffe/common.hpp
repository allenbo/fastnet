// Copyright 2013 Yangqing Jia

#ifndef CAFFE_COMMON_HPP_
#define CAFFE_COMMON_HPP_

#include <cublas_v2.h>
#include <cuda.h>
#include <curand.h>
// cuda driver types
#include <driver_types.h>
#include <stdio.h>

#define CHECK_GE(val1, val2) if ((val1) < (val2)) { \
  fprintf(stderr, #val1 " has to be greater than " #val2); \
  exit(-1); \
  }

#define CHECK(val) if ((val) == 0) { \
  fprintf(stderr, #val " has to be nonzero"); \
  exit(-1); \
  }

#define CHECK_EQ(val1, val2) if ((val1) != (val2)) {\
  fprintf(stderr, #val1 " should be equal to " #val2); \
  exit(-1); \
  }


#define LOG(x) do { fprintf(stderr, #x __FILE__ ":%d", __LINE__); \
  exit(-1); } while(0)

// various checks for different function calls.
#define CUDA_CHECK(condition) CHECK_EQ((condition), cudaSuccess)
#define CUBLAS_CHECK(condition) CHECK_EQ((condition), CUBLAS_STATUS_SUCCESS)
#define CURAND_CHECK(condition) CHECK_EQ((condition), CURAND_STATUS_SUCCESS)
#define VSL_CHECK(condition) CHECK_EQ((condition), VSL_STATUS_OK)

// After a kernel is executed, this will check the error and if there is one,
// exit loudly.
#define CUDA_POST_KERNEL_CHECK \
  if (cudaSuccess != cudaPeekAtLastError()) \
    LOG(FATAL)

// Disable the copy and assignment operator for a class.
#define DISABLE_COPY_AND_ASSIGN(classname) \
private:\
  classname(const classname&);\
  classname& operator=(const classname&)

// Instantiate a class with float and double specifications.
#define INSTANTIATE_CLASS(classname) \
  template class classname<float>; \
  template class classname<double>

// A simple macro to mark codes that are not implemented, so that when the code
// is executed we will see a fatal log.
#define NOT_IMPLEMENTED LOG(FATAL) << "Not Implemented Yet"


namespace caffe {

// We will use the boost shared_ptr instead of the new C++11 one mainly
// because cuda does not work (at least now) well with C++11 features.


// We will use 1024 threads per block, which requires cuda sm_2x or above.
#if __CUDA_ARCH__ >= 200
    const int CAFFE_CUDA_NUM_THREADS = 1024;
#else
    const int CAFFE_CUDA_NUM_THREADS = 512;
#endif



inline int CAFFE_GET_BLOCKS(const int N) {
  return (N + CAFFE_CUDA_NUM_THREADS - 1) / CAFFE_CUDA_NUM_THREADS;
}



typedef enum {CblasNoTrans=111, CblasTrans=112, CblasConjTrans=113} CBLAS_TRANSPOSE;

}  // namespace caffe

#endif  // CAFFE_COMMON_HPP_
