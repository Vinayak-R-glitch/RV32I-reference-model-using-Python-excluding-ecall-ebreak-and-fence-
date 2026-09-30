import math
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
        self.datamem={}
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
            





