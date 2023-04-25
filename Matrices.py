from fractions import Fraction

class Matrix:
	__slots__ = 'matrix','ord'

	def __init__(self,param):
		self.matrix = param
		self.ord    = [len(param),len(param[0])] # row major

	def __str__(self):
		f = [[Fraction(float(f'{self.matrix[r][c]:.9f}')).limit_denominator() for c in range(self.ord[1])] for r in range(self.ord[0])]
		x = ""
		for i in range(self.ord[0]):
			x += "[\t"
			for j in range(self.ord[1]):
				x += f"{f[i][j]}\t"
			x += "]\n"
		return x
		

	def __add__(self,param):
		__slots__ = "new","param"
		new = [[] for i in range(self.ord[0])]
		[new[i].append(self.matrix[i][j]+param.matrix[i][j]) for j in range(self.ord[1]) for i in range(self.ord[0])]
		return Matrix(new)

	def __sub__(self,param):
		__slots__ = "new","param"
		new = [[] for i in range(self.ord[0])]
		[new[i].append(self.matrix[i][j]-param.matrix[i][j]) for j in range(self.ord[1]) for i in range(self.ord[0])]
		return Matrix(new)

	def __rmul__(self,factor):
		__slots__ = "new","factor"
		new = [[] for i in range(self.ord[0])]
		[new[i].append(self.matrix[i][j]*factor) for j in range(self.ord[1]) for i in range(self.ord[0])]
		return Matrix(new)

	def __mul__(self,param):
		__slots__ = "new","param"
		new = [[[] for __ in range(param.ord[1])] for _ in range(min(self.ord[0],param.ord[0]))]
		[new[row][column].append(self.matrix[row][r]*param.matrix[r][column]) for r in range(self.ord[1]) for column in range(param.ord[1]) for row in range(self.ord[0])]
		[exec("new[i][j]=sum(new[i][j])") for j in range(len(new[0])) for i in range(len(new))]
		return Matrix(new)

	def determinant(matrix):
		__slots__ = "new", "matrix"
		try:
			new = []
			for row in range(matrix.ord[0]):
				for column in range(matrix.ord[1]):
					new.append(Matrix([[matrix.matrix[r][c] for c in range(matrix.ord[1]) if column != c] for r in range(matrix.ord[0]) if row != r]))
			if new[0].ord != [1,1]:
				new = [Matrix.determinant(new[i]) for i in range(len(new))]
			new = [matrix.matrix[0][i] * new[i] for i in range(matrix.ord[1])]
			f = 0
			for i in range(len(new)):
				if i % 2 == 0:
					f = f + new[i].matrix[0][0]
				else:
					f = f - new[i].matrix[0][0]
				
			return Matrix([[f]])
		except: return matrix

	def transpose(matrix):
		__slots__ = "new","matrix"
		new = [[] for i in range(matrix.ord[1])]
		[new[column].append(matrix.matrix[row][column]) for row in range(matrix.ord[0]) for column in range(matrix.ord[1])]
		return Matrix(new)

	def inverse(self):
		__slots__ = "new","lx","coeff","deter"
		deter = Matrix.determinant(self).matrix[0][0]
		coeff = 1/deter
		new = [[] for _ in range(self.ord[0])]
		for row in range(self.ord[0]):
			for column in range(self.ord[1]):
				new[row].append(Matrix.determinant(Matrix([[self.matrix[r][c] for c in range(self.ord[1]) if column != c] for r in range(self.ord[0]) if row != r])).matrix[0][0])
		new = Matrix.transpose(Matrix(new)).matrix
		for r in range(len(new)):
			for c in range(1-(r%2),len(new[0]),2):
				new[r][c]=new[r][c]*-1
		lx = [[] for i in range(self.ord[0])]
		[lx[i].append(new[i][j]*coeff) for j in range(self.ord[1]) for i in range(self.ord[0])]
		return Matrix(lx)
