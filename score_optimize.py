import pulp
import numpy as np
import argparse

import sys

parser = argparse.ArgumentParser(description='optimizer')
parser.add_argument('--user', '-u', type=int, default=1,
                    help='')
parser.add_argument('--jack', '-j', type=int, default=0,
                    help='')
args = parser.parse_args()
#USER = 30
#ITEM = 50
USER = 30
ITEM = 20
Users = list(range(0,USER))
Items = list(range(0,ITEM))

np.random.seed(10)
prob = pulp.LpProblem("test",pulp.LpMaximize)

#scores = np.asarray([[3,2,1,1,0],[1,2,3,1,0],[1,1,2,3,0]])
scores = np.zeros((USER,ITEM),dtype=np.float64)
scores2 = np.zeros((USER,ITEM),dtype=np.float64)
for j in Items:
    b = 5 * (j // 5) + 1
#    print("j={},b={}",j,b)
    scores[:,j] = np.random.beta(25,b,USER)
print("scores=",scores)
for i in Users:
    order = np.argsort(scores[i,:])
    for j in range(0,3):
        scores2[i][order[-j-1]] = 5
    for j in range(3,10):
        scores2[i][order[-j-1]] = 3
    for j in range(10,20):
        scores2[i][order[-j-1]] = 1
#    for j in range(20,30):
#        scores2[i][order[-j-1]] = 2
#    for j in range(30,50):
#        scores2[i][order[-j-1]] = 1
print("before:scores2=",scores2)

if args.jack == 1:
     hosei = np.zeros(ITEM,np.float64)
     hosei[18] = 0.5
     hosei[19] = 0.5
     scores2 = scores2 + hosei

print("after:scores2=",scores2)
choices = pulp.LpVariable.dicts("Choice",(Users,Items) , 0, 1, pulp.LpInteger)
print("scores={}",scores)
estimate = 0
for i in Users:
    for j in Items:
        estimate += scores2[i][j] * choices[i][j]

prob += estimate

# ユーザ制限(各ユーザ5件のみ選択)
for u in Users:
    prob += pulp.lpSum([choices[u][i] for i in Items]) == 5

if args.user == 1:
    # アイテム制限(各item10人のみ選択)
    for i in Items:
        prob += pulp.lpSum([choices[u][i] for u in Users]) <= 10

#print(prob)

status = prob.solve()
print("Status:", pulp.LpStatus[status])


choices_np = np.zeros((USER,ITEM),dtype=np.int)
for i in Users:
    for j in Items:
        choices_np[i][j] = choices[i][j].value()
print("choices_np=",choices_np)
