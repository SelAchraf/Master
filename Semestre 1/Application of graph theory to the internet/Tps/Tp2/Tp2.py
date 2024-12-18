import numpy as np

matrix_length = int(input("Enter the number of columns in the matrix: "))
lines = []
i = 1

if matrix_length <= 0:
    raise ValueError("Matrix length must be a positive integer.")

while True:
    line = input(f"Enter the line number {i}: ")
    
    if line.lower() == 'fin':
        break

    line = list(map(int, line.split()))
    if len(line) != matrix_length:
        print(f"Error: Line must contain exactly {matrix_length} elements.")
    else:
        lines.append(line)
        i += 1

if lines:
    matrix = np.array(lines)
    print("\nThe Matrix:")
    print(matrix)
else:
    print("No matrix created. You did not enter any rows.")

minimums_lines = []
for line in matrix:
    minimums_lines.append(int(min(line)))
print("\nThe minimums of the matrix lines: ")
print(minimums_lines)

j = 0
for line in matrix:
    for i in range(len(line)):
        line[i] = line[i] - minimums_lines[j]
    j += 1
print("\nThe Reduced Matrix:")
print(matrix)

minimums_columns = []
for column in matrix.T:
    minimums_columns.append(int(min(column)))
print("\nThe minimums of the matrix columns: ")
print(minimums_columns)

y = 0
for column in matrix.T:
    for i in range(len(column)):
        column[i] = column[i] - minimums_columns[y]
    y += 1
print("\nThe New Reduced Matrix:")
print(matrix)