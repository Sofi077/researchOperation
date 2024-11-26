from sympy import symbols, Eq, solve
import numpy as np
from scipy.optimize import linprog
from sympy import symbols, Eq, Gt
import numpy as np

# matrix = np.array([[3, 7, 1, -2, 2],
#                    [2, -5, -4, 0, 2],
#                    [1, 6, -3, -5, -1]])
matrix = np.array([[0, 3],
                   [1, 2],
                   [6, 1]])
# matrix = np.array([[0.4, 0.9, 0.5, 0.5, 0.6],
#                    [0.6, 0.5, 0.7, 0.8, 0.9],
#                    [0.6, 0.3, 0.8, 0.6, 0.7],
#                    [0.3, 0.8, 0.5, 0.4, 0.3],
#                    [0.1, 0.3, 0.5, 0.4, 0.3],
#                    [0.1, 0.8, 0.5, 0.4, 0.5]])
# matrix = np.array([[2, 0, 3],
#                    [1, 3, -3]])

#лічильники для рядків і стовпців
row_count = {i: 0 for i in range(len(matrix))}
row_count[0] += 1
col_count = {i: 0 for i in range(matrix.shape[1])}

row = matrix[0]
col0 = [0 for _ in range(matrix.shape[0])]
row_index = 0
n = 100000 #кількість ітерацій
for i in range(1, n):
    min_element = np.min(row)
    col_index = np.where(row == min_element)[0][0]
    v1 = min_element/i
    v1 = round(v1, 3)


    col = matrix[:, col_index] + col0

    max_element = np.max(col)

    v2 = max_element/i
    v2 = np.round(v2, 3)

    v = (v1 + v2)/2
    v = np.round(v, 3)

    print(f"{i} || {row_index + 1} | {min_element}", end='   ')
    print(f"v1 | {v1}", end='   ')
    print(f"     {col_index + 1} | {max_element}", end='   ')
    print(f"v2 | {v2}", end='   ')
    print(f"v | {v}")


    row_index = np.where(col == max_element)[0][0]
    col0 = col

    row2 = matrix[row_index] + row
    row = row2

    #оновлення лічильників
    row_count[row_index] += 1
    col_count[col_index] += 1

    if (v1==v2):
        n = i
        break
#______________________________________
# знайти останній ключ у словнику
last_key = max(row_count.keys())
# зменшити значення за цим ключем на 1
row_count[last_key] -= 1
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

print(f"\nv {v}")
print(f"Кількість ітерацій {n}")
print("\nКількість викликів рядків     X")
for idx, count in row_count.items():
    print(f"A {idx + 1}: {count} ", end='                     ')
    print(count/n)

print("\nКількість викликів стовпців   y")
for idx, count in col_count.items():
    print(f"B {idx + 1}: {count} ", end='                      ')
    print(count/n)







