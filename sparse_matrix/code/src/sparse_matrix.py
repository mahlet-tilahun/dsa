# Linked list node class for storing matrix elements
class MatrixNode:
    """
    Represents a non-zero element in the sparse matrix.
    Each node stores its row, column, value and a pointer to the next node.
    """
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value
        self.next = None


class SparseMatrix:
    """
    SparseMatrix class using a singly linked list to store non-zero elements.
    Supports addition, subtraction, and multiplication.
    """
    def __init__(self, matrix_file_path=None, num_rows=0, num_cols=0):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.head = None  # Head of the linked list

        # If file path is given, load matrix from file
        if matrix_file_path:
            self._load_from_file(matrix_file_path)

    def _load_from_file(self, file_path):
        """
        Loads a sparse matrix from a file, validates format and contents.
        """
        try:
            with open(file_path, 'r') as file:
                # Read and clean first two lines for rows and cols
                rows_line = file.readline().strip().replace(" ", "")
                cols_line = file.readline().strip().replace(" ", "")

                # Validate header format
                if not rows_line.startswith("rows=") or not cols_line.startswith("cols="):
                    raise ValueError("Input file has wrong format")

                # Extract dimensions
                try:
                    self.num_rows = int(rows_line[5:])
                    self.num_cols = int(cols_line[5:])
                except ValueError:
                    raise ValueError("Input file has wrong format")

                # Process the remaining lines (matrix elements)
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

                    # Check if coordinates are within bounds
                    if row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols:
                        raise ValueError("Matrix coordinates out of bounds")

                    # Store non-zero values
                    if value != 0:
                        self.set_element(row, col, value)
        except IOError:
            raise IOError("Could not open file")

    def get_element(self, row, col):
        """
        Returns the value at the given (row, col).
        Returns 0 if element is not stored (zero by default).
        """
        self._validate_coords(row, col)
        current = self.head
        while current:
            if current.row == row and current.col == col:
                return current.value
            current = current.next
        return 0

    def set_element(self, row, col, value):
        """
        Sets the value at the given (row, col).
        Removes node if value is zero.
        """
        self._validate_coords(row, col)

        if self.head is None:
            if value != 0:
                self.head = MatrixNode(row, col, value)
            return

        prev = None
        current = self.head
        while current:
            if current.row == row and current.col == col:
                if value == 0:
                    # Remove the node
                    if prev:
                        prev.next = current.next
                    else:
                        self.head = current.next
                else:
                    # Update value
                    current.value = value
                return
            prev = current
            current = current.next

        # Add new node at head if value is non-zero
        if value != 0:
            new_node = MatrixNode(row, col, value)
            new_node.next = self.head
            self.head = new_node

    def save_to_file(self, file_path):
        """
        Saves the matrix to a file in the given format.
        """
        try:
            with open(file_path, 'w') as file:
                file.write(f"rows={self.num_rows}\n")
                file.write(f"cols={self.num_cols}\n")

                # Collect elements into list for sorting
                elements = []
                current = self.head
                while current:
                    elements.append((current.row, current.col, current.value))
                    current = current.next

                elements.sort()  # Sort by row then col
                for row, col, value in elements:
                    file.write(f"({row}, {col}, {value})\n")
        except IOError:
            raise IOError("Could not write to file")

    def add(self, other):
        """
        Adds two matrices and returns a new SparseMatrix result.
        """
        self._validate_shape(other)
        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)

        # Copy all elements from self
        current = self.head
        while current:
            result.set_element(current.row, current.col, current.value)
            current = current.next

        # Add elements from other
        current = other.head
        while current:
            value = result.get_element(current.row, current.col) + current.value
            result.set_element(current.row, current.col, value)
            current = current.next
        return result

    def subtract(self, other):
        """
        Subtracts another matrix from this matrix.
        Returns a new SparseMatrix result.
        """
        self._validate_shape(other)
        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)

        # Copy elements from self
        current = self.head
        while current:
            result.set_element(current.row, current.col, current.value)
            current = current.next

        # Subtract elements from other
        current = other.head
        while current:
            value = result.get_element(current.row, current.col) - current.value
            result.set_element(current.row, current.col, value)
            current = current.next
        return result

    def multiply(self, other):
        """
        Multiplies this matrix with another and returns a new SparseMatrix result.
        """
        if self.num_cols != other.num_rows:
            raise ValueError("Number of columns in first matrix must equal number of rows in second matrix")

        result = SparseMatrix(num_rows=self.num_rows, num_cols=other.num_cols)
        a = self.head
        while a:
            b = other.head
            while b:
                if a.col == b.row:
                    value = result.get_element(a.row, b.col) + a.value * b.value
                    result.set_element(a.row, b.col, value)
                b = b.next
            a = a.next
        return result

    def _validate_shape(self, other):
        """
        Validates that two matrices have the same dimensions.
        """
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrix dimensions must match")

    def _validate_coords(self, row, col):
        """
        Validates that the given (row, col) coordinates are within matrix bounds.
        """
        if row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols:
            raise ValueError("Matrix coordinates out of bounds")


# Driver code
if __name__ == "__main__":
    try:
        matrix1_path = input("Enter the path for the first matrix: ")
        matrix2_path = input("Enter the path for the second matrix: ")

        print("Select operation:")
        print("1: Addition")
        print("2: Subtraction")
        print("3: Multiplication")
        operation = int(input("Enter the operation (1/2/3): "))

        output_path = input("Enter the output file path: ")

        # Load matrices from file
        matrix1 = SparseMatrix(matrix1_path)
        matrix2 = SparseMatrix(matrix2_path)

        # Perform selected operation
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

        # Save result to output file
        result.save_to_file(output_path)
        print(f"Result saved to {output_path}")

    except Exception as e:
        print(f"Error: {e}")
