from __future__ import print_function
from ortools.constraint_solver import pywrapcp

'''
制約プログラミングの練習
https://developers.google.com/optimization/mip/integer_opt_cp
'''
def main(num_buses_check=0):
    # Instantiate a CP solver.
    parameters = pywrapcp.Solver.DefaultSolverParameters()
    solver = pywrapcp.Solver("simple_CP", parameters)

    # x and y are integer non-negative variables.
    x = [solver.IntVar(0, 17, 'x'), solver.IntVar(0, 17, 'y')]
    # solver.Add(2*x[0] + 14*x[1] <= 35)
    # solver.Add(2*x[0] <= 7)
    xx = 2*x[0] + 14*x[1]
    solver.Add(xx <= 35)
    xxx = 2*x[0]
    solver.Add(xxx <= 7)
    obj_expr = solver.IntVar(0, 1000, "obj_expr")
    solver.Add(obj_expr == x[0] + 10*x[1])
    objective = solver.Maximize(obj_expr, 1)
    decision_builder = solver.Phase([x[0], x[1]],
                                    solver.CHOOSE_FIRST_UNBOUND,
                                    solver.ASSIGN_MIN_VALUE)
    # Create a solution collector.
    collector = solver.LastSolutionCollector()
    # Add the decision variables.
    collector.Add(x[0])
    collector.Add(x[1])
    # Add the objective.
    collector.AddObjective(obj_expr)
    solver.Solve(decision_builder, [objective, collector])
    if collector.SolutionCount() > 0:
        best_solution = collector.SolutionCount() - 1
        print("Objective value:", collector.ObjectiveValue(best_solution))
        print()
        print('x= ', collector.Value(best_solution, x[0]))
        print('y= ', collector.Value(best_solution, x[1]))

if __name__ == "__main__":
    main()
