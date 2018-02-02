from __future__ import print_function
import sys
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import solver_parameters_pb2
import numpy as np


def pred_sales_quantity(item_id,price,shelf_position,face):
    # なんか適当に
    intercept = 1
    sales_quantity = intercept + price/100 + shelf_position + face
    return int(sales_quantity)

'''
棚割り最適化を制約プログラミングで解いてみる
'''
def main():
    # Instantiate a CP solver.
    parameters = pywrapcp.Solver.DefaultSolverParameters()
    solver = pywrapcp.Solver("shelf_opt_CP", parameters)

    items_count = 5
    shelfs_count = 2
    face_max = 5
    d = [3,3]

    # Instantiate a CP solver.
    parameters = pywrapcp.Solver.DefaultSolverParameters()
    solver = pywrapcp.Solver("simple_CP", parameters)

    # x and y are integer non-negative variables.

    # 商品ｉを棚ｊにｋフェイス置いたら１、そうでなければ０
    x =  np.array([[[solver.BoolVar() for i in range(items_count)] for j in range(shelfs_count)] for k in range(face_max)])
    for i in range(items_count):
        con1 = 0
        for j in range(shelfs_count):
            for k in range(face_max):
                con1 += x[k, j, i]
        solver.Add(con1 <= 1)

    for j in range(shelfs_count):
        con2 = 0
        for i in range(items_count):
            for k in range(face_max):
                con2 += x[k, j, i]
        solver.Add(con2 <= d[j])

    # 商品ｉの価格
    p = np.array([solver.IntVar(0, 100, 'p') for i in range(items_count)])

    print(x)
    print(p)

    # 商品ｉを棚ｊにｋフェイス置き、価格がPijkのときの売上個数
    v =

    obj_expr = solver.IntVar(0, 100000, "obj_expr")
    obj_val = 0
    for j in range(shelfs_count):
        for i in range(items_count):
            for k in range(face_max):
                obj_val += x[k, j, i]
    solver.Add(obj_expr == obj_val)

    # solver.Add(obj_expr == x[0] + 10*x[1])
    # objective = solver.Maximize(obj_expr, 1)
    # decision_builder = solver.Phase([x[0], x[1]],
    #                                 solver.CHOOSE_FIRST_UNBOUND,
    #                                 solver.ASSIGN_MIN_VALUE)
    # # Create a solution collector.
    # collector = solver.LastSolutionCollector()
    # # Add the decision variables.
    # collector.Add(x[0])
    # collector.Add(x[1])
    # # Add the objective.
    # collector.AddObjective(obj_expr)
    # solver.Solve(decision_builder, [objective, collector])
    # if collector.SolutionCount() > 0:
    #     best_solution = collector.SolutionCount() - 1
    #     print("Objective value:", collector.ObjectiveValue(best_solution))
    #     print()
    #     print('x= ', collector.Value(best_solution, x[0]))
    #     print('y= ', collector.Value(best_solution, x[1]))




if __name__ == "__main__":
    main()
