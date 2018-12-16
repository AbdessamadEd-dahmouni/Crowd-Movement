from math import sqrt
import time
from tkinter import Tk, Canvas, Button, Label,ALL
from random import choice
#*******************Parameters*****************************#
N=200        # number of agents
r=3          # radius of agents (for the simulation) 
INF=10**6    # high value for the boundaries of the Fast Marching algorithm
X = 100      # width of the grid
Y = 75       # height of the grid
# scaling factors for the canvas 
Cx = 2*r 
Cy = 2*r
sortie=[(X-1,Y//2)] # the gate(s) (list of tuples)
#******************fonctions pour FMM**********************#
def voisinage(i,j):
    global R_init
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
    global X,Y
    if i==0:
            t1=INF
            t2=T[1][j]
    elif i==X-1:
            t1=T[X-2][j]
            t2=INF
    else:
            t1=T[i-1][j]
            t2=T[i+1][j]
            
    if j==0:
            t3=INF
            t4=T[i][1]
    elif j==Y-1:
            t3=T[i][Y-2]
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
    global X
    return (TAB!=[[1]*Y for i in range(X)])
#*********************initialisation************************#
fen1=Tk()
width=Cx*X
height=Cy*Y
can1=Canvas(fen1,height=height,width=width,bg='grey80')
x1=time.clock()    
T=[[INF]*Y for i in range(X)]
TAB=[[0]*Y for i in range(X)]
for [i,j] in sortie:
    TAB[i][j]=1
    T[i][j]=0
#*******************obstacles*******************************#
def obstacle(x1,x2,y1,y2):
    global R,TAB,obst,Cx,Cy,Y
    for i in range(x1,x2+1):
      for j in range(y1,y2+1):
        TAB[i][j]=1
        if (i,j) in R :
          R.remove((i,j))
    if obst==0:
      if y2==Y-1:
          y2=Y
      can1.create_rectangle(Cx*x1,Cy*y1,Cx*x2,Cy*y2,fill='black')
            #*************************#
R=[(i,j) for i in range(X) for j in range(Y)]
obst=0
dx = X//5
dy = Y//5
for i in range(5):
    obstacle(dx*i        ,dx*i+1*dx//4,0   ,3*dy)
    obstacle(dx*i+2*dx//4,dx*i+3*dx//4,2*dy,5*dy-1)
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
        if k>=0 and k<=X-1 and l>=0 and l<=Y-1 and TAB[k][l]!=1 and ([k,l] not in Pile_test):
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
    global objs,ps,dr,T,Cx,Cy
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
                can1.coords(cercle[i],Cx*new[0]-r,Cy*new[1]-r,Cx*new[0]+r,Cy*new[1]+r)
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
   
def initialiser():
    global objs,cercle,R,R_init,X,Y,Cx,Cy,dx,dy,obst,ps
    can1.delete(ALL)
    obst=0
    ps  =0
    objs=[]
    R=[(i,j) for i in range(X) for j in range(Y)]
    for i in range(5):
        obstacle(dx*i        ,dx*i+1*dx//4,0   ,3*dy)
        obstacle(dx*i+2*dx//4,dx*i+3*dx//4,2*dy,5*dy-1)
    R_init = R.copy()
    objs.append(choice(R))
    for i in range(1,N):
       R.remove(objs[-1])
       objs.append(choice(R))
    cercle=[]
    for obj in objs:
        cercle.append(can1.create_oval(Cx*obj[0]-r,Cy*obj[1]-r,Cx*obj[0]+r,Cy*obj[1]+r,width=1,fill='red'))
    can1.create_rectangle(3,3,width,height,width=2,outline='black')

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
    cercle.append(can1.create_oval(Cx*obj[0]-r,Cy*obj[1]-r,Cx*obj[0]+r,Cy*obj[1]+r,width=1,fill='red'))
duree=Label(fen1)
can1.create_rectangle(3,3,width,height,width=2,outline='black')
for sx,sy in sortie:
    can1.create_rectangle(Cx*(sx+1)-4,Cy*(sy-1),Cx*(sx+1)-1,Cy*(sy+1),fill='light green')
can1.grid(row=0,column=0,rowspan=6,padx=10,pady=5)
bou1=Button(fen1,text='Start'       ,width=12,command=move)
bou2=Button(fen1,text='Leave'       ,width=12,command=fen1.destroy)
bou3=Button(fen1,text='Pause/Resume',width=12,command=pause)
bou4=Button(fen1,text='Initialize'  ,width=12,command=initialiser)
bou5=Button(fen1,text='1 step'      ,width=12,command=slow)
bou1.grid(row=1,column=1,padx=5,pady=5)
bou2.grid(row=5,column=1,padx=5,pady=5)
bou3.grid(row=4,column=1,padx=5,pady=5)
bou4.grid(row=2,column=1,padx=5,pady=5)
bou5.grid(row=3,column=1,padx=5,pady=5)
duree.grid(row=0,column=1,padx=5,pady=5)
fen1.mainloop()