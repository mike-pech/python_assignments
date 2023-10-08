class Matrix:           # Точь-в-точь тот же класс из задания Ильи про матрицы. Метод ортогонализации находтися на 155 строчке 
    
    def __init__(self, matrix: list, rows: int = None, cols: int = None):
        self.matrix = matrix
        if rows is None:
            self.rows = len(self.matrix)
        else:
            self.rows = rows
        if cols is None:
            self.cols = len(self.matrix)
        else:
            self.cols = cols

    def __len__(self):
        return self.rows * self.cols

    def T(self):
        tr_matrix = [[0 for j in range(self.rows)] for i in range(self.cols)]
        for i in range(self.cols):
            for j in range(self.rows):
                tr_matrix[i][j] = self.matrix[j][i]
        return Matrix(tr_matrix)
    
    def __add__(self, other):
        if isinstance(other, Matrix):
            if self.rows == other.rows and self.cols == other.cols:
                res_matrix = []
                for i in range(self.rows):
                    temp = []
                    for j in range(self.cols):
                        temp.append(self.matrix[i][j] + other.matrix[i][j])
                    res_matrix.append(temp)
                return res_matrix
            else:
                return "Невозможно сложить матрицы разных размеров!"
        elif isinstance(other, (int, float)):
            res_matrix = []
            for i in range(self.rows):
                temp = []
                for j in range(self.cols):
                    temp.append(self.matrix[i][j] + other)
                res_matrix.append(temp)
            return res_matrix            
    
    def __sub__(self, other):
        if isinstance(other, Matrix):
            if self.rows == other.rows and self.cols == other.cols:
                res_matrix = []
                for i in range(self.rows):
                    temp = []
                    for j in range(self.cols):
                        temp.append(self.matrix[i][j] - other.matrix[i][j])
                    res_matrix.append(temp)
                return res_matrix
            else:
                return "Невозможно вычесть матрицы разных размеров!"
        elif isinstance(other, (int, float)):
            res_matrix = []
            for i in range(self.rows):
                temp = []
                for j in range(self.cols):
                    temp.append(self.matrix[i][j] - other)
                res_matrix.append(temp)
            return res_matrix            

    def __mul__(self, other):                   # Умножает соразмерные матрицы в порядке: a[i][j] * b[i][j]
        if isinstance(other, Matrix):
            if self.cols == other.cols and self.rows == other.rows:
                res_matrix = [[0 for i in range(self.cols)] for j in range(self.rows)]
                for i in range(self.rows):
                    for j in range(self.cols):
                        res_matrix[i][j] = self.matrix[i][j] * other.matrix[i][j]
                return res_matrix
            else:
                return "Невозможно умножить несоразмерные матрицы!"
        elif isinstance(other, (int, float)):
            res_matrix = []
            for i in range(self.rows):
                temp = []
                for j in range(self.cols):
                    temp.append(self.matrix[i][j] * other)
                res_matrix.append(temp)
            return res_matrix

    def __truediv__(self, other):               # Делит соразмерные матрицы в порядке: a[i][j] / b[i][j]
        if isinstance(other, Matrix):
            if self.cols == other.cols and self.rows == other.rows:
                res_matrix = [[0 for i in range(self.cols)] for j in range(self.rows)]
                for i in range(self.rows):
                    for j in range(self.cols):
                        res_matrix[i][j] = self.matrix[i][j] / other.matrix[i][j]
                return res_matrix
            else:
                return "Невозможно разделить несоразмерные матрицы!"
        elif isinstance(other, (int, float)):
            res_matrix = [[0 for i in range(self.cols)] for j in range(self.rows)]
            for i in range(self.rows):
                for j in range(self.cols):
                    res_matrix[i][j] = self.matrix[i][j] / other
            return res_matrix

    def __matmul__(self, other):                    # А вот это уже и есть умножение матриц!
        if isinstance(other, Matrix):
            if self.cols == other.rows:
                res_matrix = [[0 for i in range(other.cols)] for j in range(self.rows)]
                for i in range(self.rows):
                    for j in range(other.cols):
                        for k in range(self.cols):
                            res_matrix[i][j] += self.matrix[i][k] * other.matrix[k][j]
                return res_matrix
            else:
                return "Невозможно умножить матрицы, если количество колонок в первой не соответствует количеству рядов во второй!"
        elif isinstance(other, list):
            # mother = Matrix(other, len(other), len(other[0]))
            if self.cols == len(other):
                res_matrix = [[0 for i in range(len(other[0]))] for j in range(self.rows)]
                for i in range(self.rows):
                    for j in range(len(other[0])):
                        for k in range(self.cols):
                            res_matrix[i][j] += self.matrix[i][k] * other[k][j]
                return res_matrix
            else:
                return "Невозможно умножить матрицы, если количество колонок в первой не соответствует количеству рядов во второй!"

    def __eq__(self, other):
        if isinstance(other, Matrix):
            if self.rows == other.rows and self.cols == other.cols:
                for i in range(self.rows):
                    for j in range(other.cols):
                        if self.matrix[j][i] != other.matrix[j][i]:
                            return False
                return True
            else:
                return False
        elif isinstance(other, list[list[int]]):
            if self.rows == len(other) and self.cols == len(other[0]):
                for i in range(self.rows):
                    for j in range(self.cols):
                        if self.matrix[i][j] != other[i][j]:
                            return False
                return True
            else:
                return False
    
    def __repr__(self):
        out = ["array([", str(self.matrix[0])]
        if self.rows > 1:
            for i in range(1, self.rows):
                out.append(",\n")
                out.append("        ")
                out.append(str(self.matrix[i]))
        out.append("])")
        return "".join(out)

    def get_basis(self, basis: list = None, iteration: int = 0) -> list:
        if basis is None:
            basis = []
        if iteration == self.rows:
            result = []
            for vector in basis:
                norm = 0
                for v in vector.vector:
                    norm = norm + v**2
                norm = norm**0.5
                result.append((vector / norm).vector)
            return result
        current_basis_vector = Vector(self.T().matrix[iteration])
        for vector in basis:
            try:
                projection = vector * ((current_basis_vector @ vector) / (vector @ vector))
                current_basis_vector = current_basis_vector - projection
            except ZeroDivisionError:
                continue
        if current_basis_vector.vector.count(0) != len(current_basis_vector.vector):
            basis.append(current_basis_vector)
        return self.get_basis(basis, iteration+1)


class Vector():
    def __init__(self, vector: list, length: int = None):
        self.vector = vector
        if length is None:
            self.length = len(self.vector)
        else:
            self.length = length
        
    def __sub__(self, other):
        if isinstance(other, Vector):
            if self.length == other.length:
                res_vector = []
                for i in range(self.length):
                    res_vector.append(self.vector[i] - other.vector[i])
                return Vector(res_vector)
            else:
                return "Невозможно вычесть векторы разных размеров!"
        elif isinstance(other, (int, float)):
            res_vector = []
            for i in range(self.length):
                res_vector.append(self.vector[i] - other)
            return Vector(res_vector)            

    def __mul__(self, other):
        if isinstance(other, Vector):
            if self.length == other.length:
                res_vector = [0 for i in range(self.length)]
                for i in range(self.length):
                    res_vector[i] = self.vector[i] * other.vector[i]
                return Vector(res_vector)
            else:
                return "Невозможно умножить несоразмерные векторы!"
        elif isinstance(other, (int, float)):
            res_vector = []
            for i in range(self.length):
                res_vector.append(self.vector[i] * other)
            return Vector(res_vector)

    def __matmul__(self, other):        # Здесь -- скалярное произведение векторов
        if isinstance(other, Vector):
            if self.length == other.length:
                res_vector = [0 for i in range(self.length)]
                for i in range(self.length):
                    res_vector[i] = self.vector[i] * other.vector[i]
                return sum(res_vector)
            else:
                return "Невозможно умножить несоразмерные векторы!"
        elif isinstance(other, (int, float)):
            res_vector = []
            for i in range(self.length):
                res_vector.append(self.vector[i] * other)
            return sum(res_vector)

    def __truediv__(self, other):
        if isinstance(other, Vector):
            if self.length == other.length:
                res_vector = [0 for i in range(self.length)]
                for i in range(self.length):
                    res_vector[i] = self.vector[i] / other.vector[i]
                return Vector(res_vector)
            else:
                return "Невозможно умножить несоразмерные векторы!"
        elif isinstance(other, (int, float)):
            res_vector = []
            for i in range(self.length):
                res_vector.append(self.vector[i] / other)
            return Vector(res_vector)


if __name__ == "__main__":
    test_matrix = Matrix([[1, 1, 1, 1], [1, 2, 3, 4], [1, 3, 5, 7], [2, 4, 6, 8]])
    print(test_matrix.get_basis())