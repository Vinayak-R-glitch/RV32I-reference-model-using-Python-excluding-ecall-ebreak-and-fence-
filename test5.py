import cpu_model
""" def convhex(binnum):
    res=""
    for i in range((len(binnum)//4)+1):
        num=binnum[::-1]
        x=num[i*4:i+4][::-1]
        y=str(int("0b"+x,0))
        res+=y
    return res[::-1] """

x="0111101111"
""" def hexconv(binnum):
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
print(str(bin(int((y[::-1][0]),16))[2:])[-1:-3:-1]) """

""" def hextobin(hexstring):
    hex_only=hexstring[2::]
    binfinal=""
    for i in hex_only:
        hexbit=str(bin(int(i,16))[2::]).zfill(4)
        binfinal+=hexbit
    return binfinal

print(hextobin("0x55"))  """ 

""" print(cpu_model.hexconv(str(bin(4+int("0x"+"0000AB340",0))[2::]))) """  #need to use the address being acessed as well as teh next address to support misaligned accesses

""" def hexconv(binnum):    #converts binary string to hex string
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
            i.zfill(4) """
            


""" print(str(bin(3)[2:]).zfill(size)[-(size)::]) """

x="   hello  "
print(x)
y=x.strip()
print(y)