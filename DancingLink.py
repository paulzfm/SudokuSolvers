from time import time

class Node:
	def __init__(self, left, right, up, down, row, root):
		self.left = left
		self.right = right
		self.up = up
		self.down = down
		self.row = row
		self.root = root
		self.count = 0

	def disp(self):
		print (self.left, self.right, self.up, self.down), 'row =', self.row, 'root =', self.root

class DancingLink:
	# input: a zero_one_matrix (in boolean type) with its size (row and col)
	# output: the least rows to be selected for covering
	
	def __init__(self, zero_one_matrix, row, col):
		self.col = col
		self.row = row
		self.ans = []
		self.nodeList = []
		self.initRowCol()
		for x in range(row):
			for y in range(col):
				if zero_one_matrix[x][y]:
					self.addNode(x + 1, y + 1)

		print 'solving...'
		start = time()
		self.solve()
		end = time()
		self.time = end - start

	def initRowCol(self):
		# 0: head, 1 ~ col: column roots
		for x in range(self.col + 1):
			self.nodeList.append(Node((x + self.col) % (1 + self.col), (x + 1) % (1 + self.col), x, x, 0, x))
		
		# col + 1 ~ col + row: row roots
		for x in range(self.row):
			y = x + self.col + 1
			self.nodeList.append(Node(y, y, y, y, x + 1, None))
			
	def addNode(self, x, y):	# here x, y start from 1
		# set the new node
		left = self.nodeList[self.col + x].left
		right = self.col + x
		up = self.nodeList[y].up
		down = y
		self.nodeList[y].count += 1
		self.nodeList.append(Node(left, right, up, down, x, down))
		
		last = len(self.nodeList) - 1
		# reset the neighnors
		self.nodeList[self.nodeList[last].left].right = last
		self.nodeList[self.col + x].left = last
		self.nodeList[self.nodeList[last].up].down = last
		self.nodeList[y].up = last

	def getAnswer(self):
		return self.ans

	def getTimeCost(self):
		return float('%.4f' % self.time)

	def printAnswer(self):
		print 'Rows numbered',
		for row in self.ans:
			print row,
		print 'are selected.'

	def cover(self, index):
		self.nodeList[self.nodeList[index].left].right = self.nodeList[index].right
		self.nodeList[self.nodeList[index].right].left = self.nodeList[index].left
		
		p = self.nodeList[index].down
		while p != index:
			q = self.nodeList[p].right
			while q != p:
				self.nodeList[self.nodeList[q].up].down = self.nodeList[q].down
				self.nodeList[self.nodeList[q].down].up = self.nodeList[q].up
				self.nodeList[q].count -= 1
				q = self.nodeList[q].right
			p = self.nodeList[p].down

	def resume(self, index):
		p = self.nodeList[index].up
		while p != index:
			q = self.nodeList[p].left
			while q != p:
				self.nodeList[self.nodeList[q].up].down = q
				self.nodeList[self.nodeList[q].down].up = q
				self.nodeList[q].count += 1
				q = self.nodeList[q].left
			p = self.nodeList[p].up

		self.nodeList[self.nodeList[index].left].right = index
		self.nodeList[self.nodeList[index].right].left = index 

	def solve(self):
		if self.nodeList[0].right == 0:
			return True
		
		# find the column with the least 1
		pMin = self.nodeList[0].right
		p = self.nodeList[pMin].right
		while p != 0:
			if self.nodeList[p].count < self.nodeList[pMin].count:
				pMin = p
			p = self.nodeList[p].right
		
		# cover this column
		self.cover(pMin)

		p = self.nodeList[pMin].down
		while p != pMin:
			self.ans.append(self.nodeList[p].row)
			# cover other columns
			q = self.nodeList[p].right
			while q != p:
				if self.nodeList[q].root != None:
					self.cover(self.nodeList[q].root)
				q = self.nodeList[q].right
			if self.solve():
				return True
			else: # failed: uncover
				q = self.nodeList[p].left
				while q != p:
					if self.nodeList[q].root != None:
						self.resume(self.nodeList[q].root)
					q = self.nodeList[q].left
			p = self.nodeList[p].down

		self.resume(pMin)
		return False