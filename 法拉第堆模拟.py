import random
from matplotlib import pyplot as plt

N=25
roun=True
ln=1000  #环周期长
e=0.2     #斜角
t=0.1   #时步
p=10000   #覆盖因子

a=[[0,0,0,0,0,0]*N]  #left,h_left,x,h_x,right,h_right

def gen(lis):
    #第一步：碰撞
    newlis=[]
    for i in lis:
        l=i[0]
        lh=i[1]
        x=i[2]
        xh=i[3]
        r=i[4]
        rh=i[5]
        if l>x:
            l-=ln
        if r<x:
            r+=ln
        left=x-l
        right=r-x
        dx=t*(left-right)/(right**2+left**2)
        dlh=-dx*e*right/(left+right)
        drh=dx*e*left/(left+right)
        dxh=(drh+dlh)/2
        newlis.append([dx,dlh,drh,dxh])
    #第二步：扩散
    newlis=[newlis[-1]]+newlis+[newlis[0]]
    xmovlis=[0 for i in range(len(lis)+1)]  #定义第N个峰的左边的谷为第N个谷，注意此处指针的i是第i-1个峰
    ymovlis=[0 for i in range(len(lis)+1)]
    for i in range(1,len(newlis)-1):
        if newlis[i][1]>newlis[i-1][2]:
            xmovlis[i-1]=-(newlis[i][1]-newlis[i-1][2])/(2*e)
            ymovlis[i-1]=(newlis[i][1]+newlis[i-1][2])/2
        if newlis[i][2]>newlis[i+1][1]:
            xmovlis[i]=(newlis[i][2]-newlis[i+1][1])/(2*e)
            ymovlis[i]=(newlis[i][2]+newlis[i+1][1])/2
    if xmovlis[0]==0:
        xmovlis[0]=xmovlis[-1]
    xmovlis=xmovlis[:-1]
    if ymovlis[0]==0:
        ymovlis[0]=ymovlis[-1]
    ymovlis=ymovlis[:-1]
    #第三步：覆盖
    newlis=newlis[1:-2]
    vellis=[]
    for i in range(len(lis)):
        l=lis[i][0]
        lh=lis[i][1]
        vellis.append([(l+xmovlis[i])%ln,(lh+ymovlis[i])%ln])
    vellis=[vellis[-1]]+vellis+[vellis[0]]
    finlis=[]
    for i in range(1,len(vellis)-1):
        if vellis[i][1]>vellis[i+1][1]:
            if vellis[i][0]-vellis[i+1][0]>2*ln/3:
                bouns=ln
            else:
                bouns=0
            if e*(vellis[i+1][0]+bouns-vellis[i][0])>vellis[i][1]-vellis[i+1][1]:
                finlis.append(vellis[i])
                
        elif vellis[i][1]>vellis[i-1][1]:
            if vellis[i-1][0]-vellis[i][0]>2*ln/3:
                bouns=ln
            else:
                bouns=0
            if e*(vellis[i][0]+bouns-vellis[i-1][0])>vellis[i][1]-vellis[i-1][1]:
                finlis.append(vellis[i])
        else:
            finlis.append(vellis[i])
    #第四步：重构
    outlis=[]
    finlis=[finlis[-1]]+finlis+[finlis[0]]
    for i in range(1,len(finlis)-1):
        l=finlis[i][0]
        r=finlis[i+1][0]
        lh=finlis[i][1]
        rh=finlis[i+1][1]
        if l-r>ln/2:
            bouns=ln
        else:
            bouns=0
        xh=(e*(r-l+bouns)+lh+rh)/2
        x=((e*(r+l-bouns)-lh+rh)/(2*e)+ln)%ln
        outlis.append([l,lh,x,xh,r,rh])
    return outlis

def ini():
    finlis=[]
    for i in range(N):
        finlis.append([random.random()*ln,e*ln*random.random()/10])
    finlis=[finlis[-1]]+finlis+[finlis[0]]
    outlis=[]
    for i in range(1,len(finlis)-1):
        l=finlis[i][0]
        r=finlis[i+1][0]
        lh=finlis[i][1]
        rh=finlis[i+1][1]
        if l-r>ln/2:
            bouns=ln
        else:
            bouns=0
        xh=(e*(r-l+bouns)+lh+rh)/2
        x=((e*(r+l-bouns)-lh+rh)/(2*e)+ln)%ln
        outlis.append([l,lh,x,xh,r,rh])
    return outlis

def draww(list):
    x=[]
    y=[]
    for i in list:
        x.append(i[0])
        x.append(i[2])
        y.append(i[1])
        y.append(i[3])
    plt.plot(x,y,color="blue")
    plt.show()

X=100
time=[0 for i in range(30)]
for k in range(X):
    sand=ini()
    count=0
    while len(sand)>3:
        count+=1
        sand=gen(sand)
        time[len(sand)]+=1/X
    print(k)
    

    
    
    