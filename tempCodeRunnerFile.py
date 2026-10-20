def hexconv(binnum):    #converts binary string to hex string
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
    return a[7::]


def hexconv(binnum):
    count=0
    divstr=""
    for i in binnum[::-1]:
        if count%4==0:
            divstr+=","
            divstr+=i
        else:
            divstr+=i
        count+=1
    l=divstr[::-1].split(",")
    hexstr=""
    for i in l:
        if i!=",":
            i.zfill(4)