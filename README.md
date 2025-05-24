# Sparse Matrix Operations

##
This project uses a Sparse Matrix data structure and provides functionality to perform **Addition**, **Subtraction**, and **Multiplication** operations on large sparse matrices stored in files. 

The sparse matrix is efficiently represented using a singly linked list to store only the non-zero elements.


---

## Input File Format

Each matrix file follows this format:

rows=8433 \
cols=3180 \
(0, 381, -694) \
(0, 128, -838) \
(0, 639, 857) \
...

- `rows=` : Total number of rows in the matrix  
- `cols=` : Total number of columns in the matrix  
- `(row, col, value)` : Position and value of a non-zero element

---

## Supported Operations

- **Addition**
- **Subtraction**
- **Multiplication**

Matrix dimensions must be compatible for each operation.

---

## How to Run

1. Make sure to have your sparse matrix files on your computer.

2. Run the program:
   ```bash
   python sparse_matrix.py

3. Follow the prompts:

- Enter input file paths

- Choose the operation (1 = Add, 2 = Subtract, 3 = Multiply)

- Provide an output file path- if the file does not exist, it will be created. 