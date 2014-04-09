import caffe
from pycuda import gpuarray, driver
import numpy as np
from distbase.util import divup
import time
caffe.init()

real_time = []

image_sizes = [224, 27, 13]
filter_sizes = [7, 5, 3]
colors = [3, 96, 256]
channels = [96, 256, 384]
paddings = [0,2,1 ]
strides = [2, 1, 1]

for image_size, color, channel, padding, stride, filter_size in zip(image_sizes, colors, channels, paddings, strides, filter_sizes):
  print 'color = %d channel = %d image_size = %d' % (color, channel, image_size)
  print '%10s\t%10s' %('batch','real')
  for batch_size in [32, 64, 128, 256]:
    input_shape = (batch_size, color, image_size, image_size)
    filter_shape = (channel, color, filter_size, filter_size)
    output_size = 1 + divup(2 * padding + image_size - filter_size, stride)
    output_shape = (batch_size, channel, output_size, output_size)

    input_local = np.ndarray(input_shape).astype(np.float32)
    filter_local = np.ndarray(filter_shape).astype(np.float32)
    output_local = np.zeros(output_shape).astype(np.float32)

    input = gpuarray.to_gpu(input_local)
    filter = gpuarray.to_gpu(filter_local)
    output = gpuarray.to_gpu(output_local)

    caffe.convFilterActs(input, filter, output, image_size, output_size, output_size, -padding, stride, color, 1)
    driver.Context.synchronize()

    count = 3
    start = time.time()
    for i in range(count):
      caffe.convFilterActs(input, filter, output, image_size, output_size, output_size, -padding, stride, color, 1)
      driver.Context.synchronize()
    real_time.append((time.time() - start) / count)

    print '%10s\t%3.7f' %(batch_size, real_time[-1])
