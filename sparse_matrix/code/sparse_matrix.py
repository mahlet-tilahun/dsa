class SparseMatrix:
    def __init__(self, matrix_file_path=None, num_rows=0, num_cols=0):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.elements = {}  # Dictionary to store non-zero elements: {(row, col): value}

        if matrix_file_path:
            self._load_from_file(matrix_file_path)

    def _load_from_file(self, file_path):
        """Load a sparse matrix from a file."""
        try:
            with open(file_path, 'r') as file:
                rows_line = file.readline().strip().replace(" ", "")
                cols_line = file.readline().strip().replace(" ", "")

                if not rows_line.startswith("rows=") or not cols_line.startswith("cols="):
                    raise ValueError("Input file has wrong format")

                try:
                    self.num_rows = int(rows_line[5:])
                    self.num_cols = int(cols_line[5:])
                except ValueError:
                    raise ValueError("Input file has wrong format")

                for line in file:
                    line = line.strip().replace(" ", "")
                    if not line:
                        continue

                    if not (line.startswith('(') and line.endswith(')')):
                        raise ValueError("Input file has wrong format")

                    data = line[1:-1].split(',')

                    if len(data) != 3:
                        raise ValueError("Input file has wrong format")

                    try:
                        row = int(data[0])
                        col = int(data[1])
                        value = int(data[2])
                    except ValueError:
                        raise ValueError("Input file has wrong format")

                    if row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols:
                        raise ValueError("Matrix coordinates out of bounds")

                    if value != 0:
                        self.set_element(row, col, value)

        except IOError:
            raise IOError("Could not open file")

    def get_element(self, row, col):
        if row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols:
            raise ValueError("Matrix coordinates out of bounds")

        return self.elements.get((row, col), 0)

    def set_element(self, row, col, value):
        if row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols:
            raise ValueError("Matrix coordinates out of bounds")

        if value == 0:
            self.elements.pop((row, col), None)
        else:
            self.elements[(row, col)] = value

    def save_to_file(self, file_path):
        try:
            with open(file_path, 'w') as file:
                file.write(f"rows={self.num_rows}\n")
                file.write(f"cols={self.num_cols}\n")

                sorted_elements = sorted(self.elements.items(), key=lambda x: (x[0][0], x[0][1]))

                for (row, col), value in sorted_elements:
                    file.write(f"({row}, {col}, {value})\n")

        except IOError:
            raise IOError("Could not write to file")

    def add(self, other):
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrix dimensions must match for addition")

        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)

        for (row, col), value in self.elements.items():
            result.set_element(row, col, value)

        for (row, col), value in other.elements.items():
            current_value = result.get_element(row, col)
            result.set_element(row, col, current_value + value)

        return result

    def subtract(self, other):
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrix dimensions must match for subtraction")

        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)

        for (row, col), value in self.elements.items():
            result.set_element(row, col, value)

        for (row, col), value in other.elements.items():
            current_value = result.get_element(row, col)
            result.set_element(row, col, current_value - value)

        return result

    def multiply(self, other):
        if self.num_cols != other.num_rows:
            raise ValueError("Number of columns in first matrix must equal number of rows in second matrix")

        result = SparseMatrix(num_rows=self.num_rows, num_cols=other.num_cols)

        other_by_row = {}
        for (row, col), value in other.elements.items():
            if row not in other_by_row:
                other_by_row[row] = []
            other_by_row[row].append((col, value))

        for (row1, col1), value1 in self.elements.items():
            if col1 in other_by_row:
                for col2, value2 in other_by_row[col1]:
                    product = value1 * value2
                    current_value = result.get_element(row1, col2)
                    result.set_element(row1, col2, current_value + product)

        return result

def main():
    try:
        matrix1_path = input("Enter the path for the first matrix: ")
        matrix2_path = input("Enter the path for the second matrix: ")

        print("Select operation:")
        print("1: Addition")
        print("2: Subtraction")
        print("3: Multiplication")
        operation = int(input("Enter the operation (1/2/3): "))

        output_path = input("Enter the output file path: ")

        matrix1 = SparseMatrix(matrix1_path)
        matrix2 = SparseMatrix(matrix2_path)

        if operation == 1:
            result = matrix1.add(matrix2)
            print("Addition completed.")
        elif operation == 2:
            result = matrix1.subtract(matrix2)
            print("Subtraction completed.")
        elif operation == 3:
            result = matrix1.multiply(matrix2)
            print("Multiplication completed.")
        else:
            raise ValueError("Invalid operation selected.")

        result.save_to_file(output_path)
        print(f"Result saved to {output_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
