import numpy as np
from sympy import symbols, Eq, solve, simplify
from itertools import combinations

# A = np.array([
#     [1, -1, 1, 0],
#     [-1, 6, 4, 0],
#     [-2, -1, 3, 6],
#     [7, 6, 4, 3]
# ])
# A = np.array([[-3, 0, 4, 9, 13],
#              [14, 10, 8, 3, 2]
# ])
A = np.array([
    [-1, 2, 1],
    [2, -1, 1],
    [1, -1, 2]
])
# A = np.array([
#     [-2, 6],
#     [0, 3],
#     [5, 5],
#     [14, -3],
#     [10, 2]
# ])
# A = np.array([
#     [6, 10, 9],
#     [4, 6, 5],
#     [7, 5, 4]
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
        return False


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
        return False

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
            is_valid = inequality > 0
        else:  # якщо це вираз, спрощуємо його
            is_valid = simplify(inequality) > 0
        inequality_results.append(is_valid)

    return {"solution": solution, "inequality_results": inequality_results}


def select_matrices(A):
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
            matrix_2x2 = A[np.ix_(rows, cols)]

            if n!=2: # залишкові рядки
               remaining_rows = [i for i in range(n) if i not in rows]
               inequality_rows = A[np.ix_(remaining_rows, cols)] if remaining_rows else np.array([])


            if m!=2: #залишкові стовпці
                remaining_cols = [j for j in range(m) if j not in cols]
                inequality_cols = A[np.ix_(rows, remaining_cols)] if remaining_cols else np.array([])



            try:
                if n!=2 and m!=2:
                    resultA = solve_and_checkA(matrix_2x2, inequality_rows)
                    resultB = solve_and_checkB(matrix_2x2, inequality_cols.T)
                elif n==2 and m!=2:
                    resultA = solveA(matrix_2x2)
                    resultB = solve_and_checkB(matrix_2x2, inequality_cols.T)

                elif n!=2 and m==2:
                    resultA = solve_and_checkA(matrix_2x2, inequality_rows)
                    resultB = solveB(matrix_2x2)



                if n!=2 and m!=2:
                        if all(resultA['inequality_results']) and all(resultB['inequality_results']) and resultA['solution'][vA]==resultB['solution'][vB]:
                            vA_value = resultA.get('solution', {}).get('vA', None) if resultA else None
                            vB_value = resultB.get('solution', {}).get('vB', None) if resultB else None
                            if vA_value == vB_value:
                                print("matrix 2x2")
                                print(matrix_2x2)
                                print("resultA")
                                print(resultA)
                                print("resultB")
                                print(resultB)
                                print("\n")



                if n==2:
                    if all(resultB['inequality_results']) and resultA:
                        vA_value = resultA.get('vA', None) if resultA else None
                        vB_value = resultB.get('solution', {}).get('vB', None) if resultB else None
                        if vA_value == vB_value:
                            print("matrix 2x2")
                            print(matrix_2x2)
                            print("resultA")
                            print(resultA)
                            print("resultB")
                            print(resultB)
                            print("\n")


                if m==2:
                    if all(resultA['inequality_results']) and resultB:
                        vB_value = resultB.get('vA', None) if resultB else None
                        vA_value = resultA.get('solution', {}).get('vA', None) if resultA else None
                        if vA_value == vB_value:
                            print("matrix 2x2")
                            print(matrix_2x2)
                            print("resultA")
                            print(resultA)
                            print("resultB")
                            print(resultB)
                            print("\n")


            except Exception as e:
                continue

print("Matrix\n----------------------------------------\n")

n, m = A.shape
print(A)
print("\n")
if n==2 and m==2:
    resultA = solveA(A)
    resultB = solveB(A)
    if resultA[vA]==resultB[vB]:
        print(solveA(A))
        print(solveB(A))

elif n==3 and m==3:
    resultA = solveA(A)
    resultB = solveB(A)
    if resultA and resultB:
        vA_value = resultA.get('vA', None) if resultA else None
        vB_value = resultB.get('vB', None) if resultB else None
        if vA_value==vB_value:
            print(solveA(A))
            print(solveB(A))

    select_matrices(A)
else:
    select_matrices(A)


