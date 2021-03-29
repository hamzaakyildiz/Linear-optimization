
from copy import deepcopy

m =0  ##number of constraints
n =0  ##number of variable
c =[] ##coefficient vector
cn=[]
b=[]  ##RHS
bn=[]
A=[]  ##matrix
An=[]
B=[]  ##base matrix
B_inv=[]
x=[]
basicSet=[]
nonBasicSet=[]
c_B=[]



def exchangeRows(M,firstRow,secondRow):
    temp=M[firstRow][:]
    M[firstRow][:]=M[secondRow][:]
    M[secondRow][:]=temp
    
def multiplyRow(M,nonZeroConstant,rowNumber):
    for i in range(len(M[rowNumber])):
        M[rowNumber][i]=M[rowNumber][i]*nonZeroConstant
        
def multiplyMatrix(M, c):
    for i in range(len(M)):
        multiplyRow(M, c, i)
        
def rowOperationRow(M,firstRow,secondRow,c):
    for i in range(len(M[firstRow])):
        M[firstRow][i]=M[firstRow][i]+M[secondRow][i]*c
        
def printArr(M):
    for i in range(len(M)):
        try:
            for j in range(len(M[i])):
                print("{:.2f}".format(M[i][j]),end =" ")
            print() 
        except:
            print("{:.2f}".format(M[i]),end =" ")     
    

def pivoting(M):
    n=len(M)
    for row in range(0,n):
        col=row
        k=[]
        if M[row][col]==0:
            for j in range(row+1,n):
                if M[j][col]!=0:
                    exchangeRows(M, j, row)
                    break
        if M[row][col] == 0:
            for j in range(row+1,n)       :
                if M[row][j]!=0:
                    col=j
                    
        for i in range(row+1,n):
            if M[row][col]!=0:
                k.append(-1*M[i][col]/M[row][col])
            
        p=0
        for j in range(row+1,n):
            if len(k)!=0:
                rowOperationRow(M, j, row,k[p])
                p=p+1
 
def getInverse(M):
    if len(M)==1:
        CT=[]
        CT.append(1/M[0][0])
        return CT
    C=getCofactor(M)
    CT=getTranspose(C)
    multiplyMatrix(CT, 1/getDeterminant(M))
    return CT
      
def getDeterminant(A):
    determinant=0
    if len(A)==1:
        return A[0][0]
    if len(A)==2:
        determinant=(A[0][0]*A[1][1]-A[0][1]*A[1][0])
        return determinant
    temp=deepcopy(A)
    for i in range(len(A)):
        x=A[0][i]
        temp=deletingCol(i,A)
        temp=deletingRow(0,temp)
        determinant=determinant + x*((-1)**i)*getDeterminant(temp)
    return determinant

def getCofactor(M):
    C=deepcopy(M)           
    for i in range(len(M)):
        for j in range(len(M[i])):
            temp=deletingCol(j, M)
            temp=deletingRow(i,temp)
            C[i][j]=getDeterminant(temp)*((-1)**(i+j))
    return C        
   
def deletingCol(colNumber,M):
    temp=deepcopy(M)
    [i.pop(colNumber) for i in temp]
    return temp

def deletingRow(rowNumber,M):
    temp=[]
    for i in range(len(M)):
        if i!=rowNumber:
            temp.append(M[i])
    return temp     
      
def getTranspose(A):
    M=deepcopy(A);
    temp1=[]
    temp2=[]
    for colNumber in range(len(M[0])):
        temp1=[]
        [temp1.append(i.pop(0)) for i in M]
        temp2.append(temp1)
    return temp2

def getData(file):
    f=open(file)
    if (f.name.split(".")[1] == "txt"):
        global m,n,c,b,A,B,B_inv
        A=[]
        b=[]
        c=[]
        B=[]
        B_inv=[]
        print(file)
        line=f.readline()
        line=line.split("\t")
        line = list(map(int, line))
        m=int(line[0])
        n=int(line[1])
        line=f.readline()
        line=line.split("\t")
        c = list(map(float, line))
        for line in f:
            line=line.split("\t")
            line = list(map(float, line))
            b.append(line.pop(len(line)-1))
            A.append(line)
        return 1;
    return -1
         
def setB():
    global B,c_B,c,basicSet
    temp1=[]
    temp=deepcopy(A)
    B=[]
    c_B=[]
    for i in temp:
        for j in basicSet:
            temp1.append(i[j])
        B.append(temp1)
        temp1=[]
    for i in basicSet:
        if i>=len(c):
            c_B.append(0) 
        else:
            c_B.append(c[i])

def addSlack(M):
    global m
    for i in range(m):
        for j in range(m):
            if(j==i):
                M[i].append(1)
            else:
                M[i].append(0)
                
def pricingOut():
    global cn,n
    cn=[]
    result=[]
    a=cbB()
    for i in range(len(A[0])):
        tot=0
        for j in range(len(a)):
            tot=tot+A[j][i]*a[j]
        result.append(tot)
    for j in nonBasicSet:
        if(j>=n):
            cn.append(-result[j])
        else:
            cn.append(c[j]-result[j])
    if(min(cn)>=0):
        return -1
    return cn.index(min(cn))

def RHS():
    global B_inv,bn,b
    bn=[]
    for i in range(len(b)):
        tot=0
        for j in range(len(b)):
            tot=tot+B_inv[i][j]*b[j]
        bn.append(tot)
        
def colX(colNumber):
    global B_inv,A,x
    x=[]
    temp=deepcopy(A)
    temp1=[]
    for i in temp:
        temp1.append(i.pop(colNumber))
    for i in range(m):
        tot=0
        for j in range(m):
            tot=tot+B_inv[i][j]*temp1[j]
        x.append(tot)

def setProblem():
    global m,n,c,b,A,B,c_B,basicSet,nonBasicSet
    addSlack(A)
    basicSet=[]
    nonBasicSet=[]
    for i in range(n):
        nonBasicSet.append(i)
    for i in range(n,m+n):
        basicSet.append(i)
    setB()
        
def cbB():
    global B,c_B,B_inv
    cbB=[]
    B_inv=getInverse(B)
    for i in range(len(B)):
        tot=0
        for j in range(len(c_B)):
            tot=tot+c_B[j]*B_inv[j][i]
        cbB.append(tot)
    return cbB    

def ratioTest(colNumber):
    RHS()
    colX(colNumber)
    temp=[]
    for i in range(len(bn)):
        if(x[i]==0):
            temp.append(1000000)
        elif((bn[i]/x[i])>0):
            temp.append(bn[i]/x[i])
        else:
            temp.append(1000000)
    if min(temp)!=1000000 :
        return temp.index(min(temp))
    return -1

def minV():
    tot=0
    for i in range(len(b)):
        tot+=cbB()[i]*b[i]
    solution=[0]*(n+m)
    RHS()
    for i in range(len(basicSet)):
        solution[basicSet[i]]=bn[i]
    print("Optimal variable vector:")
    print('[',end=''),printArr(solution),print(']')   
    print("Optimal result: ")
    for i in range(m):
        c.append(0)
    print(tot,"=",c,"*",'[',end=(' ')),printArr(solution),print(']')
    return tot

def solveLP():
    global basicSet,nonBasicSet
    index_in=pricingOut()
    if index_in<0:
        return
    index_out=ratioTest(nonBasicSet[index_in])
    if index_out<0:
        return
    go_in=nonBasicSet[index_in]
    go_out=basicSet[index_out]
    basicSet[index_out]=go_in
    nonBasicSet[index_in]=go_out
    setB()
    solveLP()
    return
    
import os
entries=os.listdir(os.getcwd())
for i in entries:
    if getData(i) >0:
        setProblem()
        solveLP()
        for i in cn:
            if (i<0):
                print("not optimal")
                break
        if(i>=0):
            minV()

