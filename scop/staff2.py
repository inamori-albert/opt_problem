"""
staff2.py:
Using SCOP for solving a staff scheduling problem
Copyright (c) by Joao Pedro PEDROSO and Mikio KUBO, 2011, 2013
"""

from scop import *

m=Model()


#トライアル版用データ
periods=[1,2,3,4,5]
shifts=[0,1,2]
staffs=["A","B","C"]

var={} #list of variables
for i in staffs:
     for t in periods:
          var[i,t]=m.addVariable(name=i+str(t),domain=shifts)

LB={} #各スタッフは最低3日以上出勤する必要がある．
for i in staffs:
     LB[i]=Linear("LB_{0}".format(i),rhs=3,direction=">=") #weight is set to default (1)
     for t in periods:
          for s in range(1,len(shifts)):
               LB[i].addTerms(1,var[i,t],shifts[s])
     m.addConstraint(LB[i])

UB={} #各スタッフは1日以上休みを取る必要がある．
for i in staffs:
     UB[i]=Linear("UB_{0}".format(i),rhs=6,direction="<=") #weight is set to default (1)
     for t in periods:
          for s in range(1,len(shifts)):
               UB[i].addTerms(1,var[i,t],shifts[s])
     m.addConstraint(UB[i])

UB_night={} #各スタッフの夜勤回数は最大4回まで可能．
for i in staffs:
     UB_night[i]=Linear("UB_night_{0}".format(i),rhs=4,direction="<=") #weight is set to default (1)
     for t in periods:
          UB_night[i].addTerms(1,var[i,t],shifts[-1])
     m.addConstraint(UB_night[i])

UB_shift={} #各シフトには1人のスタッフを割り当てる必要がある．
for t in periods:
     for s in range(1,len(shifts)):
          UB_shift[t,s]=Linear("UBshift_{0}_{1}".format(t,s),rhs=1,direction="=") #weight is set to default (1)
          for i in staffs:
               UB_shift[t,s].addTerms(1,var[i,t],shifts[s])
          m.addConstraint(UB_shift[t,s])



#異なるシフトに移る場合は休みを入れる必要がある．（異なるシフトが2日間連続で行うのを禁止する制約．）
Forbid={}
for i in staffs:
     for t in periods:
          for s in range(1,len(shifts)):
            Forbid[(i,t,s)]=Linear("Forbid_{0}_{1}_{2}".format(i,t,s),rhs=1)
            Forbid[(i,t,s)].addTerms(1,var[i,t],shifts[s])
            for k in range(1,len(shifts)):
                if k!=s:
                    if t==periods[-1]:
                         Forbid[(i,t,s)].addTerms(1,var[i,1],shifts[k])  
                    else:
                         Forbid[(i,t,s)].addTerms(1,var[i,t+1],shifts[k])
            m.addConstraint(Forbid[(i,t,s)])


#シフト「昼」，「夜」は，最低2日間は連続で行う．
Cons={}
for i in staffs:
     for t in periods:
        for s in range(2,len(shifts)):
             Cons[(i,t)]=Linear("Cons_{0}_{1}".format(i,t),direction=">=")
             Cons[(i,t)].addTerms(-1,var[i,t],shifts[s])
             if t==1:
                  Cons[(i,t)].addTerms(1,var[i,periods[-1]],shifts[s])
             else:
                  Cons[(i,t)].addTerms(1,var[i,t-1],shifts[s])
             if t==periods[-1]:
                  Cons[(i,t)].addTerms(1,var[i,1],shifts[s])
             else:
                  Cons[(i,t)].addTerms(1,var[i,t+1],shifts[s])
             m.addConstraint(Cons[(i,t)])


m.Params.TimeLimit=1
sol,violated=m.optimize()

print (m)

print ("solution")
for x in sol:
    print (x,sol[x])
print ("violated constraint(s)")
for v in violated:
    print (v,violated[v])







