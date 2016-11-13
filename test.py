import pulp

problem = pulp.LpProblem('test',pulp.LpMaximize)
a = pulp.LpVariable('a', 0, 1)
b = pulp.LpVariable('b', 0, 1)
problem += a + b

problem += a >= 0
problem += b >= 0.1
problem += a + 2*b == 0.5

status = problem.solve()
print("Status={}", pulp.LpStatus[status])

print(problem)

print("Result")
print("a={}", a.value())
print("b={}", b.value())
