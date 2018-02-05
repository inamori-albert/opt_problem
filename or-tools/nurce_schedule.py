
from __future__ import print_function
import sys
from ortools.constraint_solver import pywrapcp

def main():
  # ソルバの作成
  solver = pywrapcp.Solver("schedule_shifts")

  num_nurses = 4
  num_shifts = 4     # シフトを4種類定義.0ならば働かない
  num_days = 7
  # [START]
  # シフトを入れる変数を作成
  shifts = {}

  for j in range(num_nurses):
    for i in range(num_days):
      shifts[(j, i)] = solver.IntVar(0, num_shifts - 1, "shifts(%i,%i)" % (j, i))
  shifts_flat = [shifts[(j, i)] for j in range(num_nurses) for i in range(num_days)]

  # ナースを入れる変数を作成
  nurses = {}

  for j in range(num_shifts):
    for i in range(num_days):
      nurses[(j, i)] = solver.IntVar(0, num_nurses - 1, "shift%d day%d" % (j,i))
  # シフトとナースの関係を記述
  for day in range(num_days):
    nurses_for_day = [nurses[(j, day)] for j in range(num_shifts)]

    for j in range(num_nurses):
      s = shifts[(j, day)]
      solver.Add(s.IndexOf(nurses_for_day) == j)
  # 割り当てを毎日変える
  for i in range(num_days):
    solver.Add(solver.AllDifferent([shifts[(j, i)] for j in range(num_nurses)]))
    solver.Add(solver.AllDifferent([nurses[(j, i)] for j in range(num_shifts)]))
  # 看護師は5~6日の間働く
  for j in range(num_nurses):
    solver.Add(solver.Sum([shifts[(j, i)] > 0 for i in range(num_days)]) >= 5)
    solver.Add(solver.Sum([shifts[(j, i)] > 0 for i in range(num_days)]) <= 6)
  works_shift = {}

  for i in range(num_nurses):
    for j in range(num_shifts):
      works_shift[(i, j)] = solver.BoolVar('shift%d nurse%d' % (i, j))

  for i in range(num_nurses):
    for j in range(num_shifts):
      solver.Add(works_shift[(i, j)] == solver.Max([shifts[(i, k)] == j for k in range(num_days)]))

  # For each shift (other than 0), at most 2 nurses are assigned to that shift
  # during the week.
  for j in range(1, num_shifts):
    solver.Add(solver.Sum([works_shift[(i, j)] for i in range(num_nurses)]) <= 2)
  # If s nurses works shifts 2 or 3 on, he must also work that shift the previous
  # day or the following day.
  solver.Add(solver.Max(nurses[(2, 0)] == nurses[(2, 1)], nurses[(2, 1)] == nurses[(2, 2)]) == 1)
  solver.Add(solver.Max(nurses[(2, 1)] == nurses[(2, 2)], nurses[(2, 2)] == nurses[(2, 3)]) == 1)
  solver.Add(solver.Max(nurses[(2, 2)] == nurses[(2, 3)], nurses[(2, 3)] == nurses[(2, 4)]) == 1)
  solver.Add(solver.Max(nurses[(2, 3)] == nurses[(2, 4)], nurses[(2, 4)] == nurses[(2, 5)]) == 1)
  solver.Add(solver.Max(nurses[(2, 4)] == nurses[(2, 5)], nurses[(2, 5)] == nurses[(2, 6)]) == 1)
  solver.Add(solver.Max(nurses[(2, 5)] == nurses[(2, 6)], nurses[(2, 6)] == nurses[(2, 0)]) == 1)
  solver.Add(solver.Max(nurses[(2, 6)] == nurses[(2, 0)], nurses[(2, 0)] == nurses[(2, 1)]) == 1)

  solver.Add(solver.Max(nurses[(3, 0)] == nurses[(3, 1)], nurses[(3, 1)] == nurses[(3, 2)]) == 1)
  solver.Add(solver.Max(nurses[(3, 1)] == nurses[(3, 2)], nurses[(3, 2)] == nurses[(3, 3)]) == 1)
  solver.Add(solver.Max(nurses[(3, 2)] == nurses[(3, 3)], nurses[(3, 3)] == nurses[(3, 4)]) == 1)
  solver.Add(solver.Max(nurses[(3, 3)] == nurses[(3, 4)], nurses[(3, 4)] == nurses[(3, 5)]) == 1)
  solver.Add(solver.Max(nurses[(3, 4)] == nurses[(3, 5)], nurses[(3, 5)] == nurses[(3, 6)]) == 1)
  solver.Add(solver.Max(nurses[(3, 5)] == nurses[(3, 6)], nurses[(3, 6)] == nurses[(3, 0)]) == 1)
  solver.Add(solver.Max(nurses[(3, 6)] == nurses[(3, 0)], nurses[(3, 0)] == nurses[(3, 1)]) == 1)
# decision builderを作成
  db = solver.Phase(shifts_flat, solver.CHOOSE_FIRST_UNBOUND,
                    solver.ASSIGN_MIN_VALUE)
# solution collectorを作成
  solution = solver.Assignment()
  solution.Add(shifts_flat)
  collector = solver.AllSolutionCollector(solution)

  solver.Solve(db, [collector])
  print("Solutions found:", collector.SolutionCount())
  print("Time:", solver.WallTime(), "ms")
  print()
  # いくつかの答えを表示
  a_few_solutions = [859, 2034, 5091, 7003]

  for sol in a_few_solutions:
    print("Solution number" , sol, '\n')

    for i in range(num_days):
      print("Day", i)
      for j in range(num_nurses):
        print("Nurse", j, "assigned to task",
              collector.Value(sol, shifts[(j, i)]))
      print()

if __name__ == "__main__":
  main()