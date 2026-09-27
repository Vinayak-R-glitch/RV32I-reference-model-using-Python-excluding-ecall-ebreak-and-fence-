""" def propval(num):      # pass only valid hex strings into this
    y="" 
    num2=""  
    for i in num[2::]:
        w=str(bin(int("0x"+i,0)))[2:].zfill(4) 
        num2+=w                         #if bin=1, twos complement is returned in binary, bin=0,returned as negative integer
    z=0
    flag=num2[0]
    for i in num2[::-1]:
        if z==0:
            if i=="1":
                z=1
                y+=i
            else:
                y+=i
        else:
            if i=="1":
                y+="0"
            else:
                y+="1"
    if num2[0]==0:
        return int("0b"+num2)
    else:
        return -int("0b"+y,0)   

a="0xA"
b="0xB54"
c="0x123"
print(propval(a),propval(b),propval(c)) """




def actval(num):
    w=num[2::]
    num2=""
    for i in w:
        z="0x"+i
        a=bin(int(z,0))[2::].zfill(4)
        num2+=str(a)
    if num2[0]=="1":
        num3=""
        b=0
        for i in num2[::-1]:
            if b==0:
                if i=="1":
                    b=1
                    num3+=i
                else:
                    num3+=i
            else:
                if i=="1":
                    num3+="0"
                else:
                    num3+="1"
            return num3
    else:
        return num2
    

print(actval("0xB54"))


    
