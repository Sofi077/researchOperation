import numpy as np
from sympy import symbols, Eq, solve, simplify
from itertools import combinations

A = np.array([
    [3, 2, 4, 3, 4, 5],
    [4, 2, 3, 5, 4, 2]
])
B = np.array([
    [10, 9, 7, 4, -2, -10],
    [-5, 0, 5, 8, 10 ,11]
])
# A = np.array([
#     [7, 1],
#     [6, 4],
#     [5, 5],
#     [3, 6],
#     [-2, 7]
# ])
# B = np.array([
#     [1, 6],
#     [5, 5],
#     [6, 3],
#     [7, 3],
#     [5, 8]
# ])

vA, vB = symbols('vA vB')


def solveA(A):

    #розміри матриці
    n, m = A.shape

    y_vars = symbols(f'y1:{n + 1}')

    # формуємо рівняння
    equations = []
    for i in range(n):
        row_sum = sum(A[i, j] * y_vars[j] for j in range(m))  # скалярний добуток рядка і y
        equations.append(Eq(row_sum, vA))  # додаємо рівняння: сума елементів = vA

    # сума yi = 1
    equations.append(Eq(sum(y_vars), 1))


    # розв’язок системи рівнянь
    solution = solve(equations, y_vars + (vA,))

    # перевірка на невід’ємність
    if all(solution[var] >= 0 for var in y_vars):
        return solution
    else:
        return "є від’ємні значення"


def solveB(B):

    n, m = B.shape

    x_vars = symbols(f'x1:{m + 1}')

    equations = []
    for j in range(m):  # проходимо по стовпцях
        col_sum = sum(B[i, j] * x_vars[i] for i in range(n))
        equations.append(Eq(col_sum, vB))

    equations.append(Eq(sum(x_vars), 1))


    solution = solve(equations, x_vars + (vB,))

    if all(solution[var] >= 0 for var in x_vars):
        return solution
    else:
        return "є від’ємні значення"

def solve_and_checkA(A, inequality_rows):
    """
    Розв'язує систему рівнянь та перевіряє кілька нерівностей.
    :param A: матриця коефіцієнтів (без нерівностей).
    :param inequality_rows: список рядків із коефіцієнтами для кожної нерівності.
    :return: розв’язок системи або повідомлення про невиконання нерівностей.
    """
    # розмір матриці
    n = len(A)

    y_vars = symbols(f'y1:{n + 1}')
    vA = symbols('vA')

    # формуємо рівняння
    equations = [Eq(sum(A[i][j] * y_vars[j] for j in range(n)), vA) for i in range(n)]
    equations.append(Eq(sum(y_vars), 1))



    # розв'язок системи рівнянь
    solution = solve(equations, y_vars + (vA,))

    if not solution:
        return "Система рівнянь не має розв’язків."

    for var in y_vars:
        if solution[var] < 0:
            return f"Розв’язок відхилено: {var} = {solution[var]} є від’ємним."

    # перевірка кожної нерівності
    inequality_results = []
    for inequality_row in inequality_rows:
        inequality = sum(inequality_row[j] * solution[y_vars[j]] for j in range(n)) - solution[vA]
        if simplify(inequality) < 0:
            inequality_results.append(True)
        else:
            inequality_results.append(False)


    return {"solution": solution, "inequality_results": inequality_results}






def solve_and_checkB(B, inequality_cols):
    """
    Розв'язує систему рівнянь та перевіряє кілька нерівностей.
    :param B: матриця коефіцієнтів (без нерівностей).
    :param inequality_cols: список стовпців із коефіцієнтами для кожної нерівності.
    :return: розв’язок системи або повідомлення про невиконання нерівностей.
    """
    n = len(B)
    m = len(B[0])

    x_vars = symbols(f'x1:{n + 1}')
    vB = symbols('vB')

    # формуємо рівняння по стовпцях
    equations = [Eq(sum(B[i][j] * x_vars[i] for i in range(n)), vB) for j in range(m)]
    equations.append(Eq(sum(x_vars), 1))

    solution = solve(equations, x_vars + (vB,))
    if not solution:
        return "Система рівнянь не має розв’язків."

    for var in x_vars:
        if solution[var] < 0:
            return f"Розв’язок відхилено: {var} = {solution[var]} є від’ємним."

    inequality_results = []
    for inequality_col in inequality_cols:
        inequality = sum(inequality_col[i] * solution[x_vars[i]] for i in range(n)) - solution[vB]
        if inequality.is_number:
            is_valid = inequality < 0
        else:  # якщо це вираз, спрощуємо його
            is_valid = simplify(inequality) < 0
        inequality_results.append(is_valid)

    return {"solution": solution, "inequality_results": inequality_results}


def select_matrices(A, B):
    """
    Обирає всі можливі підматриці розміру 2x2 з матриці A розміру n x m,
    та повертає залишкові рядки та стовпці для кожної ітерації.
    :param A: вхідна матриця розміру n x m.
    :return: підматриці 2x2 та відповідні залишкові рядки та стовпці
    """
    n, m = A.shape
    if n < 2 or m < 2:
        raise ValueError("Матриця занадто мала для вибору підматриць.")

    for rows in combinations(range(n), 2):  # комбінації двох рядків
        for cols in combinations(range(m), 2):  # комбінації двох стовпців
            # формуємо підматрицю 2x2
            matrixA_2x2 = A[np.ix_(rows, cols)]
            matrixB_2x2 = B[np.ix_(rows, cols)]


            if n!=2: # залишкові рядки
               remaining_rows = [i for i in range(n) if i not in rows]
               inequality_rows = A[np.ix_(remaining_rows, cols)] if remaining_rows else np.array([])

            if m!=2: #залишкові стовпці
                remaining_cols = [j for j in range(m) if j not in cols]
                inequality_cols = B[np.ix_(rows, remaining_cols)] if remaining_cols else np.array([])

            try:
                if n!=2 and m!=2:
                    resultA = solve_and_checkA(matrixA_2x2, inequality_rows)
                    resultB = solve_and_checkB(matrixB_2x2, inequality_cols.T)
                elif n==2 and m!=2:
                    resultA = solveA(matrixA_2x2)
                    resultB = solve_and_checkB(matrixB_2x2, inequality_cols.T)

                else: #m==2 and n!=2:
                    resultA = solve_and_checkA(matrixA_2x2, inequality_rows)
                    resultB = solveB(matrixB_2x2)

                if n!=2 and m!=2:
                        if all(resultA['inequality_results']) and all(resultB['inequality_results']):
                            print("Bimatrix 2x2")
                            # створення "біматриці"
                            bimatrix = np.stack((matrixA_2x2, matrixB_2x2), axis=-1)
                            #виведення
                            for row in bimatrix:
                                print(" ".join([f"({a}, {b})" for a, b in row]))

                            print("resultA")
                            print(resultA)
                            print("resultB")
                            print(resultB)
                            print("\n")


                if n==2:
                    if all(resultB['inequality_results']) and resultA:
                        print("Bimatrix 2x2")
                        bimatrix = np.stack((matrixA_2x2, matrixB_2x2), axis=-1)
                        for row in bimatrix:
                            print(" ".join([f"({a}, {b})" for a, b in row]))
                        print("resultA")
                        print(resultA)
                        print("resultB")
                        print(resultB)
                        print("\n")


                if m==2:
                    if all(resultA['inequality_results']) and resultB:
                        print("Bimatrix 2x2")
                        bimatrix = np.stack((matrixA_2x2, matrixB_2x2), axis=-1)
                        for row in bimatrix:
                            print(" ".join([f"({a}, {b})" for a, b in row]))

                        print("resultA")
                        print(resultA)
                        print("resultB")
                        print(resultB)
                        print("\n")

            except Exception as e:
                continue

print("Matrix\n----------------------------------------\n")

n, m = A.shape
bimatrix = np.stack((A, B), axis=-1)
for row in bimatrix:
    print(" ".join([f"({a}, {b})" for a, b in row]))
if n==2 and m==2:
    print(solveA(A))
    print(solveB(B))
else:

    select_matrices(A, B)
