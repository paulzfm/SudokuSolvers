from DLSolver import DLSolver
import sys

def syntaxError():
	print 'Usage:'
	print '\tpython sudoku.py [problem file name]'
	print 'or'
	print '\tpython sudoku.py [problem folder name] [sample size]'
	sys.exit()

if __name__ == "__main__":
	if len(sys.argv) == 2:
		if '.txt' in sys.argv[1]:
			DLSolver(sys.argv[1])
		else:
			syntaxError()
	elif len(sys.argv) == 3:
		size = int(sys.argv[2])
		times = []
		for index in range(size):
			print '# Problem ' + str(index + 1) + '/' + str(size) + \
			', process ' + str(100 * float('%.4f' % (float(index + 1) / size))) + '%'
			fileName = sys.argv[1] + '/' + str(index + 1) + '.txt'
			print '# File: ' + fileName
			solver = DLSolver(fileName)
			times.append(solver.getTimeCost())
		print '# Summary'
		print '# Sample Size: ' + str(size)
		print '# Average Time: ' + str(float('%.4f' % (sum(times) / size))) + 's'
		print '# Shortest Time: ' + str(min(times)) + 's'
		print '# Longest Time: ' + str(max(times)) + 's'
	else:
		syntaxError()


	# DLSolver('sample.txt')
	# zero_one = [[1, 1, 0, 0], [0, 0, 0, 1], [0, 1, 1, 1], [1, 0, 1, 0]]
	# dl = DancingLink(zero_one, 4, 4)
	# dl.printAnswer()
