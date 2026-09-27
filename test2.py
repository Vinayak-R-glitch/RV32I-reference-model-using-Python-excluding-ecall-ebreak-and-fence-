
def actval(strin):    #Pass actual hex string as argument
    stri=""
    for i in strin[2::]:
        b=str(bin(int("0x"+i,0))[2::].zfill(4))    #converting hex string to binary string
        stri+=b
    num3=''
    b=0
    flag=stri[0]                 #if number is negative find twos complement and return negative of decimal value of twos complement
    if flag=="1":
        for i in stri[::-1]:
            if b==0:
                if i=="0":
                    num3+=i
                else:
                    num3+=i
                    b=1
            else:
                if i=="1":
                    num3+="0"
                else:
                    num3+="1"
        print (-int("0b"+num3[::-1],0))
    
    else:     #if number not negative just return decimal value of number
        print(int("0b"+stri,0))

actval("0xB54")