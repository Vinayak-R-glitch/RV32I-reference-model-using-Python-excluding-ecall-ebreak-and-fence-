""" def convhex(binnum):
    res=""
    for i in range((len(binnum)//4)+1):
        num=binnum[::-1]
        x=num[i*4:i+4][::-1]
        y=str(int("0b"+x,0))
        res+=y
    return res[::-1] """

x="0111101111"
def hexconv(binnum):
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
        a+=(str(hex(int("0b"+i,0)))[2:])
    return a


y=(hexconv("0111101110"))
print(str(bin(int((y[::-1][0]),16))[2:])[-1:-3:-1])