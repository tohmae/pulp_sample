import pulp

#USER = 30
#ITEM = 50
USER = 5
ITEM = 8
users = list(range(0,USER))
items = list(range(0,ITEM))

choices = pulp.LpVariable.dicts("Choice",(users,items) , 0, 1, pulp.LpInteger)

choices[1][1] = 0

print(choices)
print(choices[1][1])
