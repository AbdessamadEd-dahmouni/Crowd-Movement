from math import sqrt
import time
from tkinter import Tk, Canvas, Button, Label
from random import choice
#*******************Parameters*****************************#
N=300
r=3
INF=10**6
M = 100
C = 6
sortie=[(M-1,M//2)]
#******************fonctions pour FMM**********************#
def voisinage(i,j):
    global M,R_init
    L = [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]
    k=0
    while k<len(L):
        if L[k] not in R_init:
            L.pop(k)
        else:
            k+=1
    return L
def resolution1(t1,t2,t3,t4):
    v1,v2=min(t1,t2),min(t3,t4)
    if abs(v1-v2)<1:
        return 0.5*(v1+v2+sqrt(2*(1**2)-(v1-v2)**2))
    else:
        return min(v1,v2)+1
def resolution2(i,j):
    global M
    if i==0:
            t1=INF
            t2=T[1][j]
    elif i==M-1:
            t1=T[M-2][i]
            t2=INF
    else:
            t1=T[i-1][j]
            t2=T[i+1][j]
            
    if j==0:
            t3=INF
            t4=T[i][1]
    elif j==M-1:
            t3=T[i][M-2]
            t4=INF
    else:
            t3=T[i][j-1]
            t4=T[i][j+1]
    return resolution1(t1,t2,t3,t4)
def calculer():
    global Pile_test,T,TAB,Pile
    for [i,j] in Pile_test :
        if TAB[i][j]!=1 :
            x=resolution2(i,j)
            if T[i][j]==INF :
                Pile.append([x,i,j])
            else :
                for (k,l) in enumerate(Pile):
                    if l[1:]==[i,j]:
                        Pile[k][0]=x
                        break
            T[i][j]=x
            TAB[i][j]=-1
def incomplet(TAB):
    global M
    return (TAB!=[[1]*M for i in range(M)])
#*********************initialisation************************#
fen1=Tk()
can1=Canvas(fen1,height=600,width=600,bg='dark grey')
x1=time.clock()    
T=[[INF]*M for i in range(M)]
TAB=[[0]*M for i in range(M)]
for [i,j] in sortie:
    TAB[i][j]=1
    T[i][j]=0
#*******************obstacles*******************************#
def obstacle(x1,x2,y1,y2):
    global R,TAB,obst,C
    for i in range(x1,x2+1):
      for j in range(y1,y2):
        TAB[i][j]=1
        if (i,j) in R :
          R.remove((i,j))
    if obst==0:
      can1.create_rectangle(C*x1,C*y1,C*x2,C*y2,fill='black')
            #*************************#
R=[(i,j) for i in range(M) for j in range(M)]
obst=0
d_obs = M//5
for i in range(5):
    obstacle(d_obs*i           ,d_obs*i+1*d_obs//4,0    ,3*d_obs+1)
    obstacle(d_obs*i+2*d_obs//4,d_obs*i+3*d_obs//4,2*d_obs,5*d_obs)
R_init=R.copy()
obst=1
#***********************Fast Marching*************************#
Pile=[]
Pile_test=[]
for [i,j] in sortie:
    L=voisinage(i,j)
    for [m,n] in L:
        if [m,n] not in Pile_test:
            Pile_test.append([m,n])
calculer()
Pile.sort()
while( incomplet(TAB) and len(Pile)>0 ):
    [i,j]=Pile[0][1:]
    v=resolution2(i,j)
    Pile.pop(0)
    T[i][j]=v
    TAB[i][j]=1
    for [k,l] in [[i-1,j],[i+1,j],[i,j-1],[i,j+1]] :
        if k>=0 and k<=M-1 and l>=0 and l<=M-1 and TAB[k][l]!=1 and ([k,l] not in Pile_test):
            Pile_test.append([k,l])
    calculer()
    Pile.sort()
x2=time.clock()
print((x2-x1))
#************************animation***************************#
def best(obj):
    m,n = obj
    L=voisinage(m,n)
    for other in objs:
        if other in L:
            L.remove(other)
    if len(L)>0:
        [k,l]=L[0]
        for [i,j] in L:
            if T[i][j]<T[k][l]:
                k,l=i,j
        return k,l
    else:
        return None

def move():
    global objs,ps,dr,T,C
    duree.configure(text=duree.configure(text='Iteration : '+str(dr)))
    if ps==0:
      finev=0
      i=0
      if len(objs)!=0:
       while i<len(objs):
           
        if  objs[i] in sortie :
            can1.delete(cercle[i])
            cercle.pop(i)
            objs.pop(i)
        else:
            new = best(objs[i])
            if new is not None:
                objs[i]=new
                finev=1
                can1.coords(cercle[i],C*new[0]-r,C*new[1]-r,C*new[0]+r,C*new[1]+r)
            i+=1
       if finev==1:
          fen1.after(20,move)
          dr+=1


def pause():
   global ps
   if ps==0:
       ps=1
   else:
       ps=0
       move()
   
def reinitialiser():
    global objs,cercle,R,R_init,M,C,d_obs
    objs=[]
    R=[(i,j) for i in range(M) for j in range(M)]
    for i in range(5):
        obstacle(d_obs*i           ,d_obs*i+1*d_obs//4,0    ,3*d_obs+1)
        obstacle(d_obs*i+2*d_obs//4,d_obs*i+3*d_obs//4,2*d_obs,5*d_obs)
    R_init = R.copy()
    objs.append(choice(R))
    for i in range(1,N):
       R.remove(objs[-1])
       objs.append(choice(R))
    cercle=[]
    for obj in objs:
        cercle.append(can1.create_oval(C*obj[0]-r,C*obj[1]-r,C*obj[0]+r,C*obj[1]+r,width=1,fill='red'))
def slow():
    global ps
    if ps==1:
        ps=0
        move()
    ps=1
#**************************graphisme****************************#
ps=0
dr=0
objs=[]
objs.append(choice(R))
for i in range(1,N):
    R.remove(objs[-1])
    objs.append(choice(R))
cercle=[]
for obj in objs:
    cercle.append(can1.create_oval(C*obj[0]-r,C*obj[1]-r,C*obj[0]+r,C*obj[1]+r,width=1,fill='red'))
duree=Label(fen1)
can1.grid(row=0,column=0,rowspan=6,padx=10,pady=5)
bou1=Button(fen1,text='Start',width=8,command=move)
bou2=Button(fen1,text='Leave',command=fen1.destroy)
bou3=Button(fen1,text='Pause/Resume',command=pause)
bou4=Button(fen1,text='Initialize',command=reinitialiser)
bou5=Button(fen1,text='1 step',command=slow)
bou1.grid(row=1,column=1,padx=5,pady=5)
bou2.grid(row=5,column=1,padx=5,pady=5)
bou3.grid(row=4,column=1,padx=5,pady=5)
bou4.grid(row=2,column=1,padx=5,pady=5)
bou5.grid(row=3,column=1,padx=5,pady=5)
duree.grid(row=0,column=1,padx=5,pady=5)
fen1.mainloop()