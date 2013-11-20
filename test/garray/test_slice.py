import garray
import numpy as np


def test_1():
  stop = 53
  a = np.random.randn(100).astype(np.float32)
  b = a[1:stop:3]
  print b

  ga = garray.array(a)
  gb = ga[1:stop:3]
  print gb

def test_2():
  a = np.random.randn(10000, 10000).astype(np.float32)
  b = a[2:10000, 3:1000]

  ga = garray.array(a)
  gb = ga[2:10000, 3:1000]

  print gb.get() - b


def test_3():
  a = np.random.randn(3, 224,224).astype(np.float32)
  b = a[:, 10:112:2, 10:112:2]

  ga = garray.array(a)
  gb = ga[:, 10:112:2, 10:112:2]

  print gb.get() - b


def test_4():
  a = np.random.randn(96, 32, 32, 128).astype(np.float32)
  b = a[:, 0:16, 0:16, :]

  ga = garray.array(a)
  gb = ga[:, 0:16, 0:16, :]

  print gb.get() - b

test_4()
