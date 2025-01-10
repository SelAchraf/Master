import numpy as np

####################################################################### Etape 0 : Réduction de la matrice initiale #######################################################################

def matrix_reduction(matrix):
    matrix = matrix - np.min(matrix, axis=1, keepdims=True)
    matrix = matrix - np.min(matrix, axis=0, keepdims=True)
    return matrix

####################################################################### Etape 1 : Encadrer et barrer les zéros #######################################################################

def frame_and_strike_zeros(reduced_matrix):
    framed = np.zeros_like(reduced_matrix, dtype=bool)
    struck = np.zeros_like(reduced_matrix, dtype=bool)
    
    while True:
        unmarked_zeros = (~struck & (reduced_matrix == 0))
        row_counts = np.sum(unmarked_zeros, axis=1)     #list
        
        if np.all(row_counts == 0):
            break
        
        min_zeros_row = np.where(row_counts == np.min(row_counts[row_counts > 0]))[0][0]
        
        zero_col = np.where(unmarked_zeros[min_zeros_row])[0][0]
        
        framed[min_zeros_row, zero_col] = True
        
        struck[:, zero_col] = np.where(
            reduced_matrix[:, zero_col] == 0, 
            True,
            False
        )  
        
        struck[min_zeros_row, :] = np.where(
            reduced_matrix[min_zeros_row, :] == 0, 
            True,
            False
        )  
        
    struck[framed] = False

    yield framed, struck

def check_optimal_solution(framed_matrix):
    if np.all(np.any(framed_matrix, axis=1)) and np.all(np.any(framed_matrix, axis=0)):
        return True
    else:
        return False

####################################################################### Etape 2 : Marquer et barrer des lignes et des colonnes #######################################################################

def mark_and_cross_out_rows_and_columns(framed_matrix, strucked_matrix):
    marked_rows = np.zeros(framed_matrix.shape[0], dtype=bool)
    marked_columns = np.zeros(framed_matrix.shape[1], dtype=bool)

    for row_idx in range(framed_matrix.shape[0]):
        if not np.any(framed_matrix[row_idx, :]):
            marked_rows[row_idx] = True

    while True:
        previous_marked_columns = marked_columns.copy()
        previous_marked_rows = marked_rows.copy() 

        for col_idx in range(strucked_matrix.shape[1]):
            if not marked_columns[col_idx]:
                if np.any(strucked_matrix[marked_rows, col_idx]):
                    marked_columns[col_idx] = True

        for row_idx in range(framed_matrix.shape[0]):
            if not marked_rows[row_idx]:
                if np.any(framed_matrix[row_idx, marked_columns]):
                    marked_rows[row_idx] = True

        if np.array_equal(previous_marked_columns, marked_columns) and np.array_equal(previous_marked_rows, marked_rows):
            break
    
    crossed_out_rows = ~marked_rows
    crossed_out_columns = marked_columns
    
    yield marked_rows, marked_columns, crossed_out_rows, crossed_out_columns

def get_partial_matrix(reduced_matrix, crossed_out_rows, crossed_out_columns):
    uncrossed_rows = ~crossed_out_rows
    uncrossed_columns = ~crossed_out_columns
    
    partial_matrix = reduced_matrix[uncrossed_rows, :][:, uncrossed_columns]
    partial_matrix_min = np.min(partial_matrix)

    yield partial_matrix, partial_matrix_min

####################################################################### Etape 3 : Modification du tableau #######################################################################

def modify_matrix(reduced_matrix, crossed_out_rows, crossed_out_columns, partial_matrix_min):
    for i in range(reduced_matrix.shape[0]):
        for j in range(reduced_matrix.shape[1]):
            if crossed_out_rows[i] and crossed_out_columns[j]:  # Double crossed
                reduced_matrix[i, j] += partial_matrix_min
            elif not crossed_out_rows[i] and not crossed_out_columns[j]:    # Not crossed
                reduced_matrix[i, j] -= partial_matrix_min
    
    return reduced_matrix

######################################################################################### Main code #########################################################################################

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
else:
    print("\nNo matrix created. You did not enter any rows.")

reduced_matrix = matrix_reduction(matrix)

while True:
    framed_matrix, strucked_matrix = next(frame_and_strike_zeros(reduced_matrix))

    if check_optimal_solution(framed_matrix):
        print(f"\nThe optimal solution is:\n{reduced_matrix}")
        break
    
    else:
        marked_rows, marked_columns, crossed_out_rows, crossed_out_columns = next(mark_and_cross_out_rows_and_columns(framed_matrix, strucked_matrix))        
        partial_matrix, partial_matrix_min = next(get_partial_matrix(reduced_matrix, crossed_out_rows, crossed_out_columns))
        reduced_matrix = modify_matrix(reduced_matrix, crossed_out_rows, crossed_out_columns, partial_matrix_min)