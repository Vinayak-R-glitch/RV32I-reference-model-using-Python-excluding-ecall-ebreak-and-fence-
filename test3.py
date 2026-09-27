x=-123
y=254
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

w=actbin(x,8)
print(w)
w=actbin(y,8)
print(w)
