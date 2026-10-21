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
        return num3[::-1].rjust(size,num3[::-1][0])[-(size)::]  
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


""" line="addi x1, x0, 10"                            #Register aliases defined by the RISC-V ABI (e.g. sp, ra, a0) are not supported; registers must be specified using the x0–x31 notation. Stack-specific pseudo-instructions and stack management are outside the scope of the assembler.
properformattemp=""                                      #
for i in line:
    if i.isalpha():
        properformattemp+=i.upper()
    elif i.isdigit():
        properformattemp+=str(i)
    elif i in [',','(',")",'-']:
        properformattemp+=i
    else:
        continue             #since hex immediates will be supported, the x from the hex string should be replace with a temporary 'h' before the validity tests
    properformat=""
    z=0  # flag for checking if the incoming immediate is hex or decimal
    for i in range(len(properformattemp)):
        if properformattemp[i]=="X":
            if properformattemp[i-1]=="0":
                properformat+="h"
                z=1
            else:
                properformat+=properformattemp[i]
        else:
            properformat+=properformattemp[i]
properformat_list=properformat.split("X")
temp=properformat_list[2]
properformat_list.pop()
properformat_list.extend(temp.split(","))
print(properformat_list) 
line="lw x5, 12(x2)"           #Register aliases defined by the RISC-V ABI (e.g. sp, ra, a0) are not supported; registers must be specified using the x0–x31 notation. Stack-specific pseudo-instructions and stack management are outside the scope of the assembler.
properformattemp=""                                      #
for i in line:
    if i.isalpha():
        properformattemp+=i.upper()
    elif i.isdigit():
        properformattemp+=str(i)
    elif i in [',','(',")",'-']:
        properformattemp+=i
    else:
        continue """             #since hex immediates will be supported, the x from the hex string should be replace with a temporary 'h' before the validity tests

""" line="addi x5, x6, 10"           #Register aliases defined by the RISC-V ABI (e.g. sp, ra, a0) are not supported; registers must be specified using the x0–x31 notation. Stack-specific pseudo-instructions and stack management are outside the scope of the assembler.
properformattemp=""                                      #
for i in line:
    if i.isalpha():
        properformattemp+=i.upper()
    elif i.isdigit():
        properformattemp+=str(i)
    elif i in [',','(',")",'-']:
        properformattemp+=i
    else:
        continue 

properformat=""
z=0  # flag for checking if the incoming immediate is hex or decimal
for i in range(len(properformattemp)):
    if properformattemp[i]=="X":
        if properformattemp[i-1]=="0":
            properformat+="h"
            z=1
        else:
            properformat+=properformattemp[i]
    else:
        properformat+=properformattemp[i]

properformat_list=properformat.split("X")
z=0
temp1=properformat_list[2]
temp2=properformat_list[1]
properformat_list.remove(temp1)
properformat_list.remove(temp2)
properformat_list.extend(temp2.strip("(").split(","))
properformat_list.append(temp1.strip(")")) 
print(properformat_list)   #list is of the form ["INSTRUCTION","RD","offset","rs1"]
try:
    if z==1:
        properformat_list[2]=int(properformat_list[3].replace("h","x"),0)
    else:
        properformat_list[2]=int(properformat_list[2])
    properformat_list[1]=int(properformat_list[1])
    properformat_list[3]=int(properformat_list[3])
except ValueError:
    print("Invalid I/S-type instruction ")

print(properformat_list)  """

""" line="addi x5, x6, 0x1A"                           #Register aliases defined by the RISC-V ABI (e.g. sp, ra, a0) are not supported; registers must be specified using the x0–x31 notation. Stack-specific pseudo-instructions and stack management are outside the scope of the assembler.
properformattemp=""                                      #
for i in line:
    if i.isalpha():
        properformattemp+=i.upper()
    elif i.isdigit():
        properformattemp+=str(i)
    elif i in [',','(',")",'-']:
        properformattemp+=i
    else:
        continue             #since hex immediates will be supported, the x from the hex string should be replace with a temporary 'h' before the validity tests
properformat=""
z=0  # flag for checking if the incoming immediate is hex or decimal
for i in range(len(properformattemp)):
    if properformattemp[i]=="X":
        if properformattemp[i-1]=="0":
            properformat+="h"
            z=1
        else:
            properformat+=properformattemp[i]
    else:
        properformat+=properformattemp[i]
properformat_list=properformat.split("X")
temp=properformat_list[2]
properformat_list.pop()
properformat_list.extend(temp.split(","))
try:
    properformat_list[1]=int(properformat_list[1].strip(','))    #removing extra comma from second register value
    properformat_list[2]=int(properformat_list[2])
    if z==1:
        properformat_list[3]=properformat_list[3].replace("h","x") 
    else:
        properformat_list[3]=int(properformat_list[3])   #converting back to proper hex
except ValueError:
    print("Invalid I-type instruction")

print(properformat_list)
print(actbin(int("0x1A",0),12)) """

print(int("0b"+"10000",0))