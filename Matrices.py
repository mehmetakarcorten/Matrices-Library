from fractions import Fraction

class Matrix:
    __slots__ = 'matrix', 'ord'

    def __init__(self, param):
        self.matrix = param
        self.ord = [len(param), len(param[0])]  # row major

    def __str__(self):
        # Convert matrix values to Fractions with limited denominators
        fractions_matrix = [[Fraction(f'{self.matrix[r][c]:.9f}').limit_denominator() for c in range(self.ord[1])] for r in range(self.ord[0])]

        # Find the maximum length of any string representation in the matrix for better alignment
        max_len = max(len(str(value)) for row in fractions_matrix for value in row)

        # Build string representation of the matrix with consistent spacing
        matrix_str = ""
        for row in fractions_matrix:
            matrix_str += "[\t" + "\t".join(f"{str(value):>{max_len}}" for value in row) + "\t]\n"
        return matrix_str


    def __add__(self, other):
        result = [[self.matrix[i][j] + other.matrix[i][j] for j in range(self.ord[1])] for i in range(self.ord[0])]
        return Matrix(result)

    def __sub__(self, other):
        result = [[self.matrix[i][j] - other.matrix[i][j] for j in range(self.ord[1])] for i in range(self.ord[0])]
        return Matrix(result)

    def __rmul__(self, factor):
        result = [[self.matrix[i][j] * factor for j in range(self.ord[1])] for i in range(self.ord[0])]
        return Matrix(result)

    def __mul__(self, other):
        result = [[sum(self.matrix[row][k] * other.matrix[k][col] for k in range(self.ord[1])) 
                   for col in range(other.ord[1])] 
                  for row in range(self.ord[0])]
        return Matrix(result)

    def determinant(self):
        if self.ord == [1, 1]:
            return self  # Base case for recursion

        det_value = 0
        for col in range(self.ord[1]):
            # Create submatrix by excluding current row and column
            submatrix = Matrix([[self.matrix[r][c] for c in range(self.ord[1]) if c != col] 
                                for r in range(1, self.ord[0])])
            sign = (-1) ** col
            det_value += sign * self.matrix[0][col] * submatrix.determinant().matrix[0][0]

        return Matrix([[det_value]])

    def transpose(self):
        transposed = [[self.matrix[row][col] for row in range(self.ord[0])] for col in range(self.ord[1])]
        return Matrix(transposed)

    def inverse(self):
        det = self.determinant().matrix[0][0]
        if det == 0:
            raise ValueError("Matrix is singular and cannot be inverted")

        # Calculate matrix of minors
        minors = [[Matrix([[self.matrix[r][c] for c in range(self.ord[1]) if c != col]
                           for r in range(self.ord[0]) if r != row]).determinant().matrix[0][0]
                   for col in range(self.ord[1])] 
                  for row in range(self.ord[0])]

        # Cofactor matrix
        cofactors = [[minors[row][col] * (-1 if (row + col) % 2 else 1)
                      for col in range(self.ord[1])] 
                     for row in range(self.ord[0])]

        # Transpose cofactor matrix
        adjugate = Matrix(cofactors).transpose().matrix

        # Multiply adjugate matrix by reciprocal of determinant
        inverse_matrix = [[adjugate[row][col] / det for col in range(self.ord[1])] for row in range(self.ord[0])]
        return Matrix(inverse_matrix)

