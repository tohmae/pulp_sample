import pulp
import numpy as np
import argparse

import sys

parser = argparse.ArgumentParser(description='optimizer')
parser.add_argument('-r', '--restrict', action='store_true', help='')
args = parser.parse_args()

USER = 30
ITEM = 20
Users = list(range(0,USER))
Items = list(range(0,ITEM))

np.random.seed(10)
scores = np.random.rand(USER, ITEM)
scores[:,0] += 0.3
scores[:,1] += 0.3
scores[:,18] -= 0.3
scores[:,19] -= 0.3
scores = np.clip(scores, 0, 1)
print(scores)

prob = pulp.LpProblem("test",pulp.LpMaximize)


# 変数の宣言
choices = pulp.LpVariable.dicts("Choice",(Users,Items) , 0, 1, pulp.LpInteger)

# 目的関数
prob += pulp.lpSum([scores[u][i] * choices[u][i] for u in Users for i in Items ])

# 制約条件
#1. $\sum_{i} choice_{ui} <= 5 (\forall u)$
for u in Users:
    prob += pulp.lpSum([choices[u][i] for i in Items]) <= 5

if args.restrict == 1:
    #2. $\sum_{u} choice_{ui} <= 10 (\forall i) $
    for i in Items:
        prob += pulp.lpSum([choices[u][i] for u in Users]) <= 10
    #3. $\sum_{u} choice_{ui} <= 3 (i=0,1) $
    for i in [0,1]:
        prob += pulp.lpSum([choices[u][i] for u in Users]) <= 3

    #4. $\sum_{u} choice_{ui} >= 9 (i=18,19) $
    for i in [18,19]:
        prob += pulp.lpSum([choices[u][i] for u in Users]) >= 9

status = prob.solve()
print("Status:", pulp.LpStatus[status])


choices_np = np.zeros((USER,ITEM),dtype=np.int)
for i in Users:
    for j in Items:
        choices_np[i][j] = choices[i][j].value()
print("choices_np=",choices_np)

for i in Users:
    choices_list = []
    for j in Items:
        choices_list.append(str(int(choices[i][j].value())))
    L = '|'.join(choices_list)
    print('|User{}|'.format(i) + L + '|')
