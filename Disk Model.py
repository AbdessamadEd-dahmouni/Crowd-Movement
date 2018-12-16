from tkinter import Tk, Canvas, Button, Label, ALL
from numpy import pi,arccos,arctan,cos,sin,sqrt
from random import choice
t=5    # temps pour faire un pas
v=0.2  #vitesse
p=v*t  # Pas
r=12   # Rayon des disques
N=120  # Nombre de gens
longueur=800
largeur=600
ys=largeur/2   #coordonnées de la sortie
xs=longueur+2*r
ps=0
temps=0
couleurs=['grey50', 'grey45', 'grey40','grey35', 'grey30','grey25','grey20','grey15','grey10']
def d(x,y,z,t):
    return sqrt((x-z)**2+(y-t)**2)
def direction(i):

    if xs>=x[i]:
      if xs==x[i] :
           if ys>y[i]:
              u=pi/2
           else:
              u=-pi/2
      else:
        u=arctan((ys-y[i])/(xs-x[i]))
        v=arccos(0.5*p/d(xs,ys,x[i],y[i]))
        T=[]
        for j in range(len(x)):
            w=d(x[i],y[i],x[j],y[j])
            if j!=i and w<p+2*r:
                if x[i]==x[j]:
                    if y[j]>y[i]:
                       T.append([pi/2,arccos((p**2+w**2-4*(r**2))/(2*w*p))])
                    else:
                       T.append([-pi/2,arccos((p**2+w**2-4*(r**2))/(2*w*p))]) 
                elif x[j]>x[i]:
                    T.append([arctan((y[j]-y[i])/(x[j]-x[i])),arccos((p**2+w**2-4*(r**2))/(2*w*p))])
                else:
                    if y[j]>y[i]:
                        T.append([pi+arctan((y[j]-y[i])/(x[j]-x[i])),arccos((p**2+w**2-4*(r**2))/(2*w*p))])
                    else:
                        T.append([arctan((y[j]-y[i])/(x[j]-x[i]))-pi,arccos((p**2+w**2-4*(r**2))/(2*w*p))])
        if x[i]<p+r :
            T.append([pi,arccos((x[i]-r)/p)])
        if longueur-x[i]<p+r and not(largeur/2.0-3*r<y[i]<largeur/2.0+3*r):
            T.append([0,arccos((longueur-x[i]-r)/p)])
        if y[i]<p+r :
            T.append([-pi/2,arccos((y[i]-r)/p)])
        if largeur-y[i]<p+r :
            T.append([pi/2,arccos((largeur-y[i]-r)/p)])
        nbcontact=len(T)
        j=0
        tour=False
        while j<len(T) :
            g=T[j]
            if g[0]-g[1]<-pi :
                tour=True
                T.pop(j)
                T.append([(g[0]+g[1]-pi)/2,(g[0]+g[1]+pi)/2])
                T.append([(g[0]-g[1]+3*pi)/2,(-g[0]+g[1]-pi)/2])
            elif g[0]+g[1]>pi  :
                tour=True
                T.pop(j)
                T.append([(g[0]-g[1]+pi)/2,(pi-g[0]+g[1])/2])
                T.append([(g[0]+g[1]-3*pi)/2,(g[0]+g[1]-pi)/2])
            else:
                j+=1
        if nbcontact==0 :
            return u,0
        else:
            o,sup,inf,s,t=1,u,u,u,u
            while o==1:
                o=0
                for [a,b] in T :
                    if a-b<sup and s<a+b :
                        s=a+b
                        o=1
                    if a-b<t and inf<a+b :
                        t=a-b
                        o=1
                sup=s
                inf=t
            if sup-u<u-inf and sup-u<=v:
                return sup,nbcontact
            if u-inf<=sup-u and u-inf<=v:
                return inf,nbcontact
        return 'bloqué',nbcontact
    else:
        u=pi+arctan((ys-y[i])/(xs-x[i]))
        v=arccos(0.5*p/d(xs,ys,x[i],y[i]))
        T=[]
        for j in range(len(x)):
            w=d(x[i],y[i],x[j],y[j])
            if j!=i and w<p+2*r:
                if x[i]==x[j]:
                    if y[j]>y[i]:
                       T.append([pi/2,arccos((p**2+w**2-4*(r**2))/(2*w*p))])
                    else:
                       T.append([3*pi/2,arccos((p**2+w**2-4*(r**2))/(2*w*p))]) 
                elif x[j]>x[i]:
                    if y[j]>y[i]:
                       T.append([arctan((y[j]-y[i])/(x[j]-x[i])),arccos((p**2+w**2-4*(r**2))/(2*w*p))])
                    else:
                       T.append([2*pi+arctan((y[j]-y[i])/(x[j]-x[i])),arccos((p**2+w**2-4*(r**2))/(2*w*p))])
                else:
                    T.append([pi+arctan((y[j]-y[i])/(x[j]-x[i])),arccos((p**2+w**2-4*(r**2))/(2*w*p))])
        if x[i]<p+r :
            T.append([pi,arccos((x[i]-r)/p)])
        if longueur-x[i]<p+r and not(largeur/2.0-3*r<y[i]<largeur/2.0+3*r):
            T.append([0,arccos((longueur-x[i]-r)/p)])
        if y[i]<p+r :
            T.append([3*pi/2,arccos((y[i]-r)/p)])
        if largeur-y[i]<p+r :
            T.append([pi/2,arccos((largeur-y[i]-r)/p)])
        nbcontact=len(T)
        j=0
        while j<len(T) :
            g=T[j]
            if g[0]-g[1]<0 :
                T.pop(j)
                T.append([(g[0]+g[1])/2,(g[0]+g[1])/2])
                T.append([2*pi+(g[0]-g[1])/2,(g[1]-g[0])/2])
            elif g[0]+g[1]>2*pi  :
                T.pop(j)
                T.append([(g[0]+g[1]-2*pi)/2,(g[0]+g[1]-2*pi)/2])
                T.append([(g[0]-g[1]+2*pi)/2,(2*pi-g[0]+g[1])/2])
            else:
                j+=1
        if nbcontact==0 :
             return u,0
        else:
            o,sup,inf,s,t=1,u,u,u,u
            while o==1:
                o=0
                for [a,b] in T :
                    if a-b<sup and s<a+b :
                        s=a+b
                        o=1
                    if a-b<t and inf<a+b :
                        t=a-b
                        o=1
                sup=s
                inf=t
            if sup-u<u-inf and sup-u<=v:
                return sup,nbcontact
            if u-inf<=sup-u and u-inf<=v:
                return inf,nbcontact
        return 'bloqué',nbcontact
    
def move():
    global x,y,ps,cercle,temps
    if ps==0:
      finev=0
      i=0
      c=0
      while i<len(x) :
        if d(x[i],y[i],xs,ys)>2*r:
            z=direction(i)
            c+=z[1]
            if z[0]!='bloqué' :
                x[i]=x[i]+p*cos(z[0])
                y[i]=y[i]+p*sin(z[0])
                can1.coords(cercle[i][0],x[i]-r,y[i]-r,x[i]+r,y[i]+r)
                can1.coords(cercle[i][1],x[i],y[i],x[i]+r*cos(z[0]),y[i]+r*sin(z[0]))
                can1.itemconfigure(cercle[i][0],fill=couleurs[z[1]])
                can1.itemconfigure(cercle[i][1],fill='red')
                finev=1
            i+=1
        else :
            can1.delete(cercle[i][0])
            can1.delete(cercle[i][1])
            cercle.pop(i)
            x.pop(i)
            y.pop(i)
      temps+=1
      duree.configure(text='Time : '+str(temps*5)+' ms')
      nombre.configure(text='Number : '+str(len(x)))
      contacts.configure(text='Collisions : '+str(c//2))
      if finev==1:
        fen1.after(t,move)

def initialiser():
    global x,y,cercle,R,temps
    temps=0
    x=[0]*N
    y=[0]*N
    R=[[i,j]for i in range(1,longueur//(2*r)) for j in range(1,largeur//(2*r))]
    [x[0],y[0]]=choice(R)
    for i in range(1,N):
        R.remove([x[i-1],y[i-1]])
        [x[i],y[i]]=choice(R)
    for i in range(N):
        x[i],y[i]=2*r*x[i],2*r*y[i]
    can1.delete(ALL)
    can1.create_rectangle(3,3,longueur,largeur,width=2,outline='black')
    can1.create_rectangle(longueur-1,largeur/2.0-4*r,longueur+2,largeur/2.0+4*r,fill='red')
    cercle=[]
    for i in range(N):
        cercle.append([can1.create_oval(x[i]-r,y[i]-r,x[i]+r,y[i]+r,width=1,fill='black'),can1.create_line(x[i],y[i],x[i]+r,y[i],width=1,fill='red')])
def pause():
   global ps
   if ps==0:
       ps=1
   else:
       ps=0
       move()
def slow():
    global ps
    if ps==1:
        ps=0
        move()
    ps=1

fen1=Tk()
can1=Canvas(fen1,height=largeur,width=longueur,bg='grey80')
x=[0]*N
y=[0]*N
R=[[i,j]for i in range(1,longueur//(2*r)) for j in range(1,largeur//(2*r))]
[x[0],y[0]]=choice(R)
for i in range(1,N):
    R.remove([x[i-1],y[i-1]])
    [x[i],y[i]]=choice(R)
for i in range(N):
    x[i],y[i]=2*r*x[i],2*r*y[i]
cercle=[]
for i in range(N):
    cercle.append([can1.create_oval(x[i]-r,y[i]-r,x[i]+r,y[i]+r,width=1,fill='black'),can1.create_line(x[i],y[i],x[i]+r,y[i],width=1,fill='red')])
can1.create_rectangle(3,3,longueur,largeur,width=2,outline='black')
can1.create_rectangle(longueur-1,largeur/2.0-4*r,longueur+2,largeur/2.0+4*r,fill='red')
can1.grid(row=0,column=0,rowspan=8)
duree=Label(fen1,width=20)
nombre=Label(fen1,width=20)
contacts=Label(fen1,width=20)
bou0=Button(fen1,text='Start',command=move)
bou1=Button(fen1,text='Pause/Resume',command=pause)
bou2=Button(fen1,text='Initialize',command=initialiser)
bou3=Button(fen1,text='1 step',command=slow)
bou4=Button(fen1,text='Quit',command=fen1.destroy)

duree.grid(row=0,column=1,padx=5,pady=5)
nombre.grid(row=1,column=1,padx=5,pady=5)
contacts.grid(row=2,column=1,padx=5,pady=5)
bou0.grid(row=3,column=1,padx=5,pady=5)
bou1.grid(row=4,column=1,padx=5,pady=5)
bou2.grid(row=5,column=1,padx=5,pady=5)
bou3.grid(row=6,column=1,padx=5,pady=5)
bou4.grid(row=7,column=1,padx=5,pady=5)

fen1.mainloop()
