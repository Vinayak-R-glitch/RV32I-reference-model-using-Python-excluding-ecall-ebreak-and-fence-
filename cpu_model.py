import math
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
        a+=(str(hex(int("0b"+i,0)))[2:])
    return a
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


class rv32i_core:
    def __init__(self):
        self.pc=0x00000000
        self.regfile=[0]*31
        self.datamem={}   #memory is modelled as a dictionary, it contains addresses in hex format and each address maps to a 32 bit binary data, memory is byte addressed
    def decode_execute(self,instruction):
        instr=instruction[1]
        opcode=instr[25:]
        if opcode=="0110011":      #instruction is r type
            rd=bintoint(instr[20:25])
            rdval=bintoint(self.regfile[rd])
            rs1=bintoint(instr[12:17])
            rs1val=bintoint(self.regfile[rs1])
            rs2=bintoint(instr[7:12])
            rs2val=bintoint(self.regfile[rs2])
            funct3=instr[17:21]
            funct7=instr[0:7]
            if funct3=="000":
                if funct7=="0000000":     #add
                    self.regfile[rd]=actbin(rs1val+rs2val,32)
                elif funct7=="0100000":    #sub
                    self.regfile[rd]=actbin(rs1val-rs2val,32)
                else:
                    print("error; invalid instruction")  #no need for elif blocks since assembler only allows two kinds of values to pass anyway
                    return
            elif funct3=="001":    #sll-logical left shift
                shiftval=bintoint((self.regfile[rs2])[27:])  #only las 5 bits of rs2 are considered as the shift value
                shiftres=rs1val*int((math.pow(2,shiftval)))  #shifting a binary number by n places is equivalent to multiplying its value by 2^n
                shiftresbin=actbin(shiftres,32)         #convert the value back to binary,restrict size to 32 bits
                self.regfile[rd]=shiftresbin
                
            elif funct3=="010":     #slt-set less than-signed
                res=int(rs1val<rs2val)
                self.regfile[rd]=actbin(res,32)
            elif funct3=="011":      #sltu-set less than unsigned
                res=int(int("0b"+self.regfile[rs1],0)<int("0b"+self.regfile[rs2],0))
                self.regfile[rd]=actbin(res,32)
            elif funct3=="100":       #xor
                res=rs1val^rs2val
                self.regfile[rd]=actbin(res,32)
            elif funct3=="101":      
                if funct7=="0000000":    #srl-right logical shift
                    reversed_bin=(self.regfile[rs1])[::-1]
                    shiftval=bintoint((self.regfile[rs2])[27:])  #only las 5 bits of rs2 are considered as the shift value
                    shiftres=bintoint(reversed_bin)*int((math.pow(2,shiftval)))  #shifting a binary number by n places is equivalent to multiplying its value by 2^n
                    shiftresbin=actbin(shiftres,32)         #convert the value back to binary,restrict size to 32 bits
                    self.regfile[rd]=shiftresbin

                elif funct7=="0100000":   #sra-rigHt arithmetic shfit
                    reversed_bin=(self.regfile[rs1])[::-1]
                    shiftval=bintoint((self.regfile[rs2])[27:])  #only las 5 bits of rs2 are considered as the shift value
                    shiftres=bintoint(reversed_bin)*int((math.pow(2,shiftval)))  #shifting a binary number by n places is equivalent to multiplying its value by 2^n
                    shiftresbin=actbin(shiftres,32)
                    if self.regfile[rs1][0]=="1":
                        shiftresfinal="1"*shiftval+shiftresbin[shiftval:]
                    else:
                        shiftresfinal="0"*shiftval+shiftresbin[shiftval:]
                    self.regfile[rd]=shiftresfinal
                else:
                    print("Error, unidentified instruction")
            elif funct3=="110":     #bitwise OR
                res=rs1val|rs2val
                self.regfile[rd]=actbin(res,32)
            elif funct3=="111":    #bitwise AND
                res=rs1val&rs2val
                self.regfile[rd]=actbin(res,32)
            else:
                print("error: invalid instruction")
                return

        elif opcode=="0010011":
            imm=instr[0:12]
            rs1=bintoint(instr[12:17])
            rs1val=bintoint(self.regfile[rs1])
            funct3=instr[17:20]
            rd=bintoint(instr[20:25])
            rdval=actbin(self.regfile[rd])
            immval=bintoint(imm)
            if funct3=="000":   #addi
                res=immval+rs1val
                resbin=actbin(res,32)
                self.regfile[rd]=resbin
            elif funct3=="010":   #slti-signed compare
                res=int(rs1val<immval)
                self.regfile[rd]=res
            elif funct3=="011":   #sltu-unsigned compare
                res=int(int("0b"+self.regfile[rs1],0)<int("0b"+imm,0))
                self.regfile[rd]=res
            elif funct3=="100":  #xori
                res=actbin(rs1val^immval,32)
                self.regfile[rd]=res
            elif funct3=="110":  #ori
                res=actbin(rs1val|immval,32)
                self.regfile[rd]=res
            elif funct3=="111":  #andi
                res=actbin(rs1val&immval,32)
                self
            elif funct3=="001": #slli- logical left shift by immediate amount
                shiftval=bintoint((imm)[8:])   
                shiftres=rs1val*int((math.pow(2,shiftval)))  
                shiftresbin=actbin(shiftres,32)         
                self.regfile[rd]=shiftresbin
            elif funct3=="101":
                if imm[1:8]=="0000000":  #srli
                    reversed_bin=(self.regfile[rs1])[::-1]
                    shiftval=bintoint(imm[8:])  
                    shiftres=bintoint(reversed_bin)*int((math.pow(2,shiftval))) 
                    shiftresbin=actbin(shiftres,32)         
                    self.regfile[rd]=shiftresbin
                elif imm[1:8]=="0100000":   #srai
                    reversed_bin=(self.regfile[rs1])[::-1]
                    shiftval=bintoint(imm[8:])  #only las 5 bits of rs2 are considered as the shift value
                    shiftres=bintoint(reversed_bin)*int((math.pow(2,shiftval)))  #shifting a binary number by n places is equivalent to multiplying its value by 2^n
                    shiftresbin=actbin(shiftres,32)
                    if self.regfile[rs1][0]=="1":
                        shiftresfinal="1"*shiftval+shiftresbin[shiftval:]
                    else:
                        shiftresfinal="0"*shiftval+shiftresbin[shiftval:]
                    self.regfile[rd]=shiftresfinal
                else:
                    print("invalid instruction")
                    return
            else:
                print("invalid instruction")

        elif opcode=="0000011":
            imm=instr[0:12]
            rs1=bintoint(instr[12:17])
            rs1val=bintoint(self.regfile[rs1])
            funct3=instr[17:20]
            rd=bintoint(instr[20:25])
            rdval=actbin(self.regfile[rd])
            immval=bintoint(imm)
            memadr=actbin(immval+rs1val,32)
            memadrhextemp=hexconv(memadr)
            def convtoproper(memadrhextemp):
                if memadrhextemp[-1] in ["0","1","2","3"]:    #routing misalgined accesses to an existing valid address, if byte 0x1003 is about to be accessed, then we find the data stored in 0x1000(divisible by 4) and take its appropriate bits
                    memadrhex=memadrhextemp[0:len(memadrhextemp)-1]+"0"
                elif memadrhextemp[-1] in ["4","5","6","7"]:
                    memadrhex=memadrhextemp[0:len(memadrhextemp)-1]+"4"
                elif memadrhextemp[-1] in ["8","9","A","B"]:
                    memadrhex=memadrhextemp[0:len(memadrhextemp)-1]+"8"
                elif memadrhextemp[-1] in ["C","D","E","F"]:
                    memadrhex=memadrhextemp[0:len(memadrhextemp)-1]+"C"
                else:
                    print("Invalid instruction")
                    return
                return memadrhex
            memadrhex=convtoproper(memadrhextemp)
            memadrhexnext=hexconv(str(bin(4+int("0x"+memadrhex,0))[2::]))  #need to use the address being acessed as well as teh next address to support misaligned accesses

            if funct3=="000" or funct3=="100":   #loadbyte or load byte unsigned
                if memadrhex in self.datamem:
                    if memadr[-2:]=="00":
                        self.regfile[rd]=self.datamem[memadrhex][24:].zfill(32) if funct3=="100" else self.datamem[memadrhex][24:][0]*24+self.datamem[memadrhex][24:]
                    elif memadr[-2:]=="01":
                        self.regfile[rd]=self.datamem[memadrhex][16:24].zfill(32) if funct3=="100" else self.datamem[memadrhex][16:24][0]*24+self.datamem[memadrhex][16:24]
                    elif memadr[-2:]=="10":
                        self.regfile[rd]=self.datamem[memadrhex][8:16].zfill(32) if funct3=="100" else self.datamem[memadrhex][8:16][0]*24+self.datamem[memadrhex][8:16]
                    elif memadr[-2:]=="11":
                        self.regfile[rd]=self.datamem[memadrhex][0:8].zfill(32) if funct3=="100" else self.datamem[memadrhex][0:8][0]*24+self.datamem[memadrhex][0:8]
                    else:
                        print("invalid address")
                else:
                    self.regfile[rd]="0".zfill(32)

            elif funct3=="001" or funct3=="101":   #load half word or load half word unsigned
                if memadrhex in self.datamem:
                    if memadr[-2:]=="00":
                        self.regfile[rd]=self.datamem[memadrhex][16:].zfill(32)  if funct3=="100" else self.datamem[memadrhex][16:][0]*16+self.datamem[memadrhex][16:]
                    elif memadr[-2:]=="01":
                        self.regfile[rd]=self.datamem[memadrhex][8:24].zfill(32) if funct3=="100" else self.datamem[memadrhex][8:24][0]*16+self.datamem[memadrhex][8:24]
                    elif memadr[-2:]=="10":
                        self.regfile[rd]=self.datamem[memadrhex][0:15].zfill(32) if funct3=="100" else self.datamem[memadrhex][0:15][0]*16+self.datamem[memadrhex][0:15]
                    elif memadr[-2:]=="11":
                        self.regfile[rd]=(self.datamem[memadrhexnext][24:]+self.datamem[memadrhex][0:7]).zfill(32)  if funct3=="100" else (self.datamem[memadrhexnext][24:][0]*16+self.datamem[memadrhexnext][24:]+self.datamem[memadrhex][0:7])
                    else:
                        print("Invalid address")
                else:
                    self.regfile[rd]="0".zfill(32)

            elif funct3=="010":   #Load word
                if memadrhex in self.datamem:
                    if memadr[-2:]=="00":
                        self.regfile[rd]=self.datamem[memadrhex][0:].zfill(32)
                    elif memadr[-2:]=="01":
                        self.regfile[rd]=(self.datamem[memadrhexnext][24:]+self.datamem[memadrhex][0:24]).zfill(32)
                    elif memadr[-2:]=="10":
                        self.regfile[rd]=(self.datamem[memadrhexnext][16:]+self.datamem[memadrhex][0:16]).zfill(32)
                    elif memadr[-2:]=="11":
                        self.regfile[rd]=(self.datamem[memadrhexnext][8:]+self.datamem[memadrhex][0:24]).zfill(32)
                    else:
                        print("Invalid address")
                else:
                    self.regfile[rd]="0".zfill(32)

                
                

                    

            






