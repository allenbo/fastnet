import varray as va
import numpy as np
import sys
import time
start = time.time()

assert len(sys.argv) == 2


# input shape should be 96 * 55 * 55 * 128
# output shape shoudl be 96 * 27 * 27 * 128
# define the parameters
start = 0
size = 3
stride = 2
out_shape = (96, 27, 27, 128)

# get the input and filter
import garray as arr
with open('filter') as f, open('input') as i:
  import cPickle as pickle
  input = pickle.load(i)
print  'read', time.time() - start

image_y = 55
output_y = 27
output_x = 27

if sys.argv[1] == 'single':
  print 'single GPU version'
  # single GPU version
  input = arr.array(input, dtype = np.float32)
  output = arr.zeros(out_shape, dtype = np.float32)

  output = arr.reshape_last(output)

  arr.avgpool(
      arr.reshape_last(input),
      output,
      96, size, start, stride, image_y, output_y, output_x)
  print  'avg pooling', time.time() - start

  output = output.reshape(out_shape)
  with open('avg-output-single', 'w') as f:
    pickle.dump(output.get(), f, protocol = -1)
  print  'done with single',time.time() - start

else:
  print 'multi GPU version'

  # get the input and filter again
  import varray as arr
  from varray import rank

  # multi GPU version
  input = arr.square_array(input, slice_dim = (1, 2))
  output = arr.zeros(out_shape, slice_dim = (1, 2))
  arr.avgpool(input,output,
      96, size, start, stride, image_y, output_y, output_x)
  print 'avg pooling', time.time() - start
  output.gather()
  if rank == 0:
    with open('avg-output-multi', 'w') as f:
      pickle.dump(output.local_data.get(), f, protocol = -1)
  print 'done with multi', time.time() - start