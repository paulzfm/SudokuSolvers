from SudokuSolver import *
from time import time

def testOne(mode, string):
  if mode == 'B':
    BacktraceSolver(string)
  elif mode == 'D':
    DFSSolver(string)
  elif mode == 'G':
    GreedySolver(string)
  else:
    print 'Mode Error'

def testAll(string):
  print 'Backtrace...'
  start = time()
  s = BacktraceSolver(string)
  end = time()
  print 'depth:',s.callingCount
  print end - start
  
  """
  print 'DFS...'
  start = time()
  s = DFSSolver(string)
  end = time()
  print 'depth:',s.callingCount
  print end - start
  """
  
  print 'Greedy...'
  start = time()
  s = GreedySolver(string)
  end = time()
  print 'depth:',s.callingCount
  print end - start

if __name__ == '__main__':
  #testAll('samples_by_level/hardest_f.txt')
  testOne(1, 'sample.txt')
