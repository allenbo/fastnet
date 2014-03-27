import math

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def isinteger(value):
  try:
    int(value)
    return True
  except ValueError:
    return False

def divup(x, base):
  if x / base * base == x:
    return int(x / base)
  else:
    return int(x / base + 1)

def issquare(x):
  a = math.sqrt(x) 
  b = int(a)
  return a == b
