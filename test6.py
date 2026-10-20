def actbin(num,size):  #handles wraparounds if immval+rsval exceeds a 32 bit value. so the hexconv function deosnt have to cover the overflow cases
    if num<0:
        num=+num
        num2=str(bin(num)[2:]) #take unsigned binary however large the number is
        b=0
        num3=""     #find twos complement of the n bit number
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
        return num3[::-1].zfill(size)[-(size)::] 
    else:
        return (str(bin(num)[2:]).zfill(size)[-(size)::])

def hexconv(binnum,size):    #converts binary string to hex string
    y=""
    for i in range(1,len(binnum)+1):
        if i%4==0:
            y+=binnum[::-1][i-1]
            y+=","
        else:
            y+=binnum[::-1][i-1]
    z=y[::-1].split(",")
    for i in range(len(z)):
        k=z[i].zfill(4)
        z[i]=k
    a=""
    for i in z:
        a+=(str(hex(int("0b"+i,0)))[2:].upper())
    return a[-size:]
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

def hextobin(hexstring):
    hex_only=hexstring[2::]
    binfinal=""
    for i in hex_only:
        hexbit=str(bin(int(i,16))[2::]).zfill(4)
        binfinal+=hexbit
    return binfinal
print(bintoint("1000"))
print(int("0b"+"1000",0))