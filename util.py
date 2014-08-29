import sys
import inspect
import copy

class SudokuMatrix:
  
  """
  This is the specially designed data structure for sudoku matrix.
  It contains a list with 81 integers, which are elements for the matrix.
  1~9 for the filled-in numbers and 0 for the blank.
  
  You need to create a matrix by loading a .txt file. The numbers should be 
  separated by space(s) and different rows should be on different lines.
  
  The construtor will anto-check whether your file is suitable for a sudoku
  problem, or exceptions will be raised.
  
  As the name indicates, there are a few useful method you can use to get rows,
  columns and small sudokus. You can get and set an element by both index and
  coordinates.
  
  The method 'isValid()' can check the validity of the latest fill-in number 
  according to the basic rule of sudoku-there can be no repeated numbers in rows,
  colunms, and small sudokus.
  """
  
  def __init__(self, fileName):
    # read into buffer
    f = open(fileName)
    buf = f.readlines()
    f.close()
    
    # change into integer list
    self.list = []
    for line in buf:
      vals = (line.split('\n'))[0].split(' ')
      for val in vals:
        if val in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
          self.list.append(int(val))
    
    # check
    if len(self.list) != 81:
      raiseMatrixFileError()
    
    # get number of blanks
    self.blank = 0
    for num in self.list:
      if num == 0:
        self.blank += 1
        
    self.digits = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
           
  def getNumByIndex(self, index):
    if index < 0 or index > 80:
      raiseOutOfRange()
    return self.list[index]
    
  def getNumByPos(self, row, col):
    if row < 0 or row > 8 or col < 0 or col > 8:
      raiseOutOfRange()
    return self.list[row * 9 + col]
  
  def setNumByIndex(self, index, num):
    if index < 0 or index > 80:
      raiseOutOfRange()
    self.list[index] = num
  
  def setNumByPos(self, row, col, num):
    if row < 0 or row > 8 or col < 0 or col > 8:
      raiseOutOfRange()
    self.list[row * 9 + col] = num
    
  def resetNum(self, index):
    if index < 0 or index > 80:
      raiseOutOfRange()
    self.list[index] = 0
    
  def display(self):
    for row in range(9):
      for col in range(9):
        print self.getNumByPos(row, col),
      print ''
        
  def getRow(self, row):
    if row < 0 or row > 8:
      raiseOutOfRange()
    return [self.getNumByPos(row, i) for i in range(9)]
  
  def getRowAsDict(self, row):
    if row < 0 or row > 8:
      raiseOutOfRange()
    dic = {}
    for i in range(9):
      num = self.getNumByPos(row, i)
      if num != 0:
        dic[row * 9 + i] = num
    return dic
  
  def getCol(self, col):
    if col < 0 or col > 8:
      raiseOutOfRange()
    return [self.getNumByPos(i, col) for i in range(9)]
    
  def getColAsDict(self, col):
    if col < 0 or col > 8:
      raiseOutOfRange()
    dic = {}
    for i in range(9):
      num = self.getNumByPos(i, col)
      if num != 0:
        dic[i * 9 + col] = self.getNumByPos(i, col)
    return dic
    
  def getBlock(self, index):
    if index < 0 or index > 8:
      raiseOutOfRange()
    row = index / 3
    col = index % 3
    list = []
    for i in range(3):
      for j in range(3):
        list.append(self.getNumByPos(row * 3 + i, col * 3 + j))
    return list
    
  def getBlockAsDict(self, index):
    if index < 0 or index > 8:
      raiseOutOfRange()
    row = index / 3
    col = index % 3
    dic = {}
    for i in range(3):
      for j in range(3):
        row_ = row * 3 + i
        col_ = col * 3 + j
        num = self.getNumByPos(row_, col_)
        if num != 0:
          dic[row_ * 9 + col_] = num
    return dic
    
  def isBlank(self, index):
    if index < 0 or index > 80:
      raiseOutOfRange()
      
    if self.getNumByIndex(index) == 0:
      return True
    return False
    
  def getWorkingIndexes(self):
    indexes = []
    for i in range(81):
      if self.isBlank(i):
        indexes.append(i)
    return indexes
    
  def isValid(self, index, num):
    if index < 0 or index > 80:
      raiseOutOfRange()
  
    row = index / 9
    col = index % 9
    
    # row checking
    for i in range(9):
      if (row * 9 + i) != index and self.list[row * 9 + i] == num:
        return False
     
    # col checking
    for i in range(9):
      if (i * 9 + col) != index and self.list[i * 9 + col] == num:
        return False
    
    # 3*3 checking
    row_s = row / 3
    col_s = col / 3
    for i in range(row_s * 3, row_s * 3 + 3):
      for j in range(col_s * 3, col_s * 3 + 3):
        if (i * 9 + j) != index and self.list[i * 9 + j] == num:
          return False
          
    return True
    
  def getPossibleNum(self, index):
    if index < 0 or index > 80:
      raiseOutOfRange()
      
    tmp = self.list[index]
    self.list[index] = 0
    row = index / 9
    col = index % 9
    rows = self.getRow(row)
    cols = self.getCol(col)
    blocks = self.getBlock((row / 3) * 3 + (col / 3))
    self.list[index] = tmp
    return list(self.digits - set(rows) - set(cols) - set(blocks) - set([0]))
  
  def isAnswer(self):
    for num in self.list:
      if num == 0:
        return False
    return True

# Get the next element after the current one. Return None
# if not found, return the first element if curr = 0
def getNext(array, curr):
  if curr == 0:
    if len(array) != 0:
      return array[0]
    else:
      return None
  
  if curr not in array:
    raise 'BIG!'
      
      
  for i in range(len(array)):
    if array[i] == curr and i != (len(array) - 1):
      return array[i + 1]
  return None
    

##################################
## from Berkeley Pacman Project ##
##################################

class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0

class Counter(dict):
    """
    A counter keeps track of counts for a set of keys.

    The counter class is an extension of the standard python
    dictionary type.  It is specialized to have number values
    (integers or floats), and includes a handful of additional
    functions to ease the task of counting data.  In particular,
    all keys are defaulted to have value 0.  Using a dictionary:

    a = {}
    print a['test']

    would give an error, while the Counter class analogue:

    >>> a = Counter()
    >>> print a['test']
    0

    returns the default 0 value. Note that to reference a key
    that you know is contained in the counter,
    you can still use the dictionary syntax:

    >>> a = Counter()
    >>> a['test'] = 2
    >>> print a['test']
    2

    This is very useful for counting things without initializing their counts,
    see for example:

    >>> a['blah'] += 1
    >>> print a['blah']
    1

    The counter also includes additional functionality useful in implementing
    the classifiers for this assignment.  Two counters can be added,
    subtracted or multiplied together.  See below for details.  They can
    also be normalized and their total count and arg max can be extracted.
    """
    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)

    def incrementAll(self, keys, count):
        """
        Increments all elements of keys by the same count.

        >>> a = Counter()
        >>> a.incrementAll(['one','two', 'three'], 1)
        >>> a['one']
        1
        >>> a['two']
        1
        """
        for key in keys:
            self[key] += count

    def argMax(self):
        """
        Returns the key with the highest value.
        """
        if len(self.keys()) == 0: return None
        all = self.items()
        values = [x[1] for x in all]
        maxIndex = values.index(max(values))
        return all[maxIndex][0]
        
    def argMin(self):
        """
        Returns the key with the least value.
        """
        if len(self.keys()) == 0: return None
        all = self.items()
        values = [x[1] for x in all]
        minIndex = values.index(min(values))
        return all[minIndex][0]

    def sortedKeys(self):
        """
        Returns a list of keys sorted by their values.  Keys
        with the highest values will appear first.

        >>> a = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> a['third'] = 1
        >>> a.sortedKeys()
        ['second', 'third', 'first']
        """
        sortedItems = self.items()
        compare = lambda x, y:  sign(y[1] - x[1])
        sortedItems.sort(cmp=compare)
        return [x[0] for x in sortedItems]

    def totalCount(self):
        """
        Returns the sum of counts for all keys.
        """
        return sum(self.values())

    def normalize(self):
        """
        Edits the counter such that the total count of all
        keys sums to 1.  The ratio of counts for all keys
        will remain the same. Note that normalizing an empty
        Counter will result in an error.
        """
        total = float(self.totalCount())
        if total == 0: return
        for key in self.keys():
            self[key] = self[key] / total

    def divideAll(self, divisor):
        """
        Divides all counts by divisor
        """
        divisor = float(divisor)
        for key in self:
            self[key] /= divisor

    def copy(self):
        """
        Returns a copy of the counter
        """
        return Counter(dict.copy(self))

    def __mul__(self, y ):
        """
        Multiplying two counters gives the dot product of their vectors where
        each unique label is a vector element.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['second'] = 5
        >>> a['third'] = 1.5
        >>> a['fourth'] = 2.5
        >>> a * b
        14
        """
        sum = 0
        x = self
        if len(x) > len(y):
            x,y = y,x
        for key in x:
            if key not in y:
                continue
            sum += x[key] * y[key]
        return sum

    def __radd__(self, y):
        """
        Adding another counter to a counter increments the current counter
        by the values stored in the second counter.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['third'] = 1
        >>> a += b
        >>> a['first']
        1
        """
        for key, value in y.items():
            self[key] += value

    def __add__( self, y ):
        """
        Adding two counters gives a counter with the union of all keys and
        counts of the second added to counts of the first.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['third'] = 1
        >>> (a + b)['first']
        1
        """
        addend = Counter()
        for key in self:
            if key in y:
                addend[key] = self[key] + y[key]
            else:
                addend[key] = self[key]
        for key in y:
            if key in self:
                continue
            addend[key] = y[key]
        return addend

    def __sub__( self, y ):
        """
        Subtracting a counter from another gives a counter with the union of all keys and
        counts of the second subtracted from counts of the first.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['third'] = 1
        >>> (a - b)['first']
        -5
        """
        addend = Counter()
        for key in self:
            if key in y:
                addend[key] = self[key] - y[key]
            else:
                addend[key] = self[key]
        for key in y:
            if key in self:
                continue
            addend[key] = -1 * y[key]
        return addend

"""
The following are some exception dealings.
"""    

def raiseOutOfRange():
  print 'List out of range.'
  sys.exit(1)

def raiseNotDefined():
  print "Method not implemented: %s" % inspect.stack()[1][3]
  sys.exit(1)
    
def raiseMatrixFileError():
  print 'Sudoku matrix file error. Please make sure your file is in right format.'
  sys.exit(1)
