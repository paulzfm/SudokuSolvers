from DancingLink import DancingLink
from util import SudokuMatrix

class DLSolver:
	def __init__(self, fileName):
		# read problem
		prob = SudokuMatrix(fileName)
		print 'PROBLEM\n======='
		prob.display()
		
		# generate zero-one matrix
		self.matrix = [[False for j in range(324)] for i in range(729)]
		for i in range(81):
			num = prob.getNumByIndex(i)
			if num == 0:
				for j in range(1, 10):
					self.set(i, j)
			else:
				self.set(i, num)

		# solve by using DL
		dl = DancingLink(self.matrix, 729, 324)

		# print time cost
		self.cost = dl.getTimeCost()
		print 'time cost:', self.cost, 's'

		# generate answer
		ans = dl.getAnswer()
		for row in ans:
			row -= 1
			prob.setNumByIndex(row / 9, row % 9 + 1)
		print 'RESULT\n======'
		prob.display()

	def getTimeCost(self):
		return self.cost

	def set(self, index, num):
		r = index * 9 + num - 1
		row = index / 9
		col = index % 9
		box = row / 3 * 3 + col / 3
		self.matrix[r][index] = True
		self.matrix[r][81 + row * 9 + num - 1] = True
		self.matrix[r][162 + col * 9 + num - 1] = True
		self.matrix[r][243 + box * 9 + num - 1] = True