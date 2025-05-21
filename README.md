Data Structures and Algorithms for Engineers
Programming Assignment 2: Sparse Matrix

Task Description: Using any programming language of your choice.
1. Load two sparse matrices from an input file.
2. Perform addition, subtraction, and multiplication on the matrices.

Instructions
1) Download the code and sample data for this assignment from this location.
. Organize the code and the sample input into the following locations:
/dsa/sparse_matrix/code/src/
/dsa/sparse_matrix /sample_inputs/
Feel free to organize your code or files the way you want.
2) Implement code to:
a) Read a sparse matrix from a file. The format of the file will be:
rows=8433
cols=3180
(0, 381, -694)
(0, 128, -838)
(0, 639, 857)
(0, 165, -933)
(0, 1350, -89)
The first row gives the number of rows. The second row gives the number of
columns. From the third row onwards, there is one entry in parenthesis with row,
column, and the integer value separated by commas. All other values in the matrix
will be zero by default. For example, in the given sample, the number of rows is
8433, the number of columns is 3180. Row 0 and column 381 has the value -694.
Row 0 and column 128 has the value -838, and so on.
b) Your goal is to implement a data structure that optimizes both memory and run time
while storing such large matrices. 