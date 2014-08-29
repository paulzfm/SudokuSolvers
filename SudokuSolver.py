# Solvers for Sudoku.

from util import *
import copy
import ctypes
import string

class SudokuSolver:
  def __init__(self, fileName):
    self.problem = SudokuMatrix(fileName)
    self.showProblem()
    self.working = copy.deepcopy(self.problem)
    self.result = None
    if self.solve():
      self.showResult()
      pass
    else:
      self.result = None
      print 'no solutions found'
    
  def getBlankCount(self):
    return self.problem.blank
      
  def solve(self):
    raiseNotDefined()

  def showProblem(self):
    print '--------Problem--------'
    self.problem.display()
  
  def showResult(self):
    print '--------Result--------'
    self.result.display()

class BacktraceSolver(SudokuSolver):
  def __init__(self, fileName):
    SudokuSolver.__init__(self, fileName)
  
  def solve(self):
    self.workingIndexes = self.problem.getWorkingIndexes()
    self.workingIndex = 0; # The index in working indexes, not in working set!
    self.callingCount = 0
    
    while True:
      if self.workingIndex == len(self.workingIndexes):	 # sulution found
        self.result = copy.deepcopy(self.working)
        return True
        
      self.trying()
      
  def trying(self):
    self.callingCount += 1
    #print 'count = ', self.callingCount
    #self.working.display()
    
    num = self.working.getNumByIndex(self.workingIndexes[self.workingIndex])
    while num != 9:
      num += 1
      if self.working.isValid(self.workingIndexes[self.workingIndex], num):		# valid
        self.working.setNumByIndex(self.workingIndexes[self.workingIndex], num)
        self.workingIndex += 1	# go to next depth
        return
        
    # no valid answer found
    # reset this index as not solved and backtrace
    self.working.resetNum(self.workingIndexes[self.workingIndex])
    self.workingIndex -= 1
    
    
class DFSSolver(SudokuSolver):
  def __init__(self, fileName):
    SudokuSolver.__init__(self, fileName)
  
  def solve(self):
    self.workingIndexes = self.problem.getWorkingIndexes()
    self.workingIndex = 0; # The index in working indexes, not in working set!
    self.callingCount = 0
    
    while True:
      if self.workingIndex == len(self.workingIndexes):	 # sulution found
        self.result = copy.deepcopy(self.working)
        return True
        
      self.trying()

  def trying(self):
    self.callingCount += 1
    
    num = self.working.getNumByIndex(self.workingIndexes[self.workingIndex])
    possibleDigits = self.working.getPossibleNum(self.workingIndexes[self.workingIndex])
    next = getNext(possibleDigits, num)
    if next != None:
      self.working.setNumByIndex(self.workingIndexes[self.workingIndex], next)
      self.workingIndex += 1	# go to next depth
      return
        
    # no valid answer found
    # reset this index as not solved and backtrace
    self.working.resetNum(self.workingIndexes[self.workingIndex])
    self.workingIndex -= 1
  
    
class GreedySolver(SudokuSolver):
  def _init__(self, fileName):
    SudokuSolver.__init__(self, fileName)
    
  def getPossibleNumDict(self):
    dic = {}
    for index in self.working.getWorkingIndexes():
      dic[index] = copy.deepcopy(self.working.getPossibleNum(index))
    return dic
    
  # only one possible digit
  def onlyOneSolver(self):
    flag = True
    while flag:
      self.callingCount += 1
      flag = False
      for (index, digits) in self.getPossibleNumDict().items():
        if len(digits) == 1:
          self.working.setNumByIndex(index, digits[0])
          flag = True
    return None
  
  # find the digit which only appear once in the dictionary
  def unique(self, dic):
    digits = []
    unique = []
    
    for key in dic:
      for ele in dic[key]:
        digits.append(ele)
    
    for digit in digits:
      if digits.count(digit) == 1:
        unique.append(digit)
    
    results = {}
    for num in unique:
      for pos in dic: 
        if num in dic[pos]:
          results[pos] = num
    
    return results
  
  
  # collect elements by row, col, block in all possible numbers dictionary
  def collectRow(self, row):
    possible = self.getPossibleNumDict()
    dic = {}
    for key in possible:
      if key / 9 == row:
        dic[key] = copy.deepcopy(possible[key])
    return dic
  
  def collectCol(self, col):
    possible = self.getPossibleNumDict()
    dic = {}
    for key in possible:
      if key % 9 == col:
        dic[key] = copy.deepcopy(possible[key])
    return dic
    
  def collectBlock(self, index):
    possible = self.getPossibleNumDict()
    dic = {}
    for key in possible:
      col = key / 9 / 3
      row = key % 9 / 3
      if (row * 3 + col) == index:
        dic[key] = copy.deepcopy(possible[key])
    return dic
  
  # find the hidden only one digit
  # If the digit only appears once in a row, col, block. The digit must
  # be there.
  def hiddenSolver(self):
    flag = True
    count = 0
    
    while flag:
      count += 1
      self.callingCount += 1
    
      flag = False
      
      # row
      for i in range(9):
        unique = self.unique(self.collectRow(i))
        if len(unique) != 0:
          flag = True
          for index in unique.keys():
            self.working.setNumByIndex(index, unique[index])
    
      # col
      for i in range(9):
        unique = self.unique(self.collectCol(i))
        if len(unique) != 0:
          flag = True
          for index in unique.keys():
            self.working.setNumByIndex(index, unique[index])
               
      # block
      for i in range(9):
        unique = self.unique(self.collectBlock(i))
        if len(unique) != 0:
          flag = True
          for index in unique.keys():
            self.working.setNumByIndex(index, unique[index])
      
      if count == 1:
        return False
      self.onlyOneSolver()   
    return True
  
  def solve(self):
    self.callingCount = 0
    self.onlyOneSolver()
    while True:
      ans = self.hiddenSolver()
      if self.working.isAnswer():
        break
      if ans == False:
        return False
    self.result = copy.deepcopy(self.working)
    return True