""" import math
x="00001001010101010101000110111101"
def actbin(num,size):
    if num<0:
        num=+num
        num2=str(bin(num)[2:]).zfill(size)
        b=0
        num3=""
        for i in num2[::-1]:
            if b==0:
                if i=="1":
                    num3+=i
                    b=1
                else:
                    num3+=i
            else:
                if i=="1":
                    num3+="0"
                else:
                    num3+="1"
        return num3[::-1]
    else:
        return str(bin(num)[2:]).zfill(size)

def bintoint(binnum):
    sign=binnum[0]
    if sign=="1":
        b=0
        num3=""
        for i in binnum[::-1]:
            if b==0:
                if i=="1":
                    num3+=i
                    b=1
                else:
                    num3+=i
            else:
                if i=="1":
                    num3+="0"
                else:
                    num3+="1"
        return -int("0b"+num3[::-1],0)
    else:
        return int("0b"+binnum,0)

#x<<4
y=bintoint(x)
y*=int(math.pow(2,4))
z=actbin(y,32)
print(z) """

""" y=int(int("0b"+"1001",0)<int("0b"+"1111",0))
print(y) """

x="10101110"
y=(x[1:5])[::-1]
print(y)
