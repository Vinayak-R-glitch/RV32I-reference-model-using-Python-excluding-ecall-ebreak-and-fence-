import math
def convtoproper(memadrhextemp):
    if memadrhextemp[-1] in ["0","1","2","3"]:    #routing misalgined accesses to an existing valid address, if byte 0x1003 is about to be accessed, then we find the data stored in 0x1000(divisible by 4) and take its appropriate bits
        memadrhex=memadrhextemp[0:len(memadrhextemp)-1]+"0"
    elif memadrhextemp[-1] in ["4","5","6","7"]:
        memadrhex=memadrhextemp[0:len(memadrhextemp)-1]+"4"
    elif memadrhextemp[-1] in ["8","9","a","b"]:
        memadrhex=memadrhextemp[0:len(memadrhextemp)-1]+"8"
    elif memadrhextemp[-1] in ["c","d","e","f"]:
        memadrhex=memadrhextemp[0:len(memadrhextemp)-1]+"c"
    else:
        print("Invalid instruction")
        return
    return memadrhex
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
        a+=(str(hex(int("0b"+i,2)))[2:])
    return a[-8:]
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

class rv32i_core:
    def __init__(self):
        self.pc="00000000"
        self.regfile=["0"*32]*32
        self.datamem={}   #memory is modelled as a dictionary, it contains addresses in hex format and each address maps to a 32 bit binary data, memory is byte addressed
    def decode_execute(self,instruction):   #data memory is also 32 wide, i.e 2^32 possible addresses will be all
        instr=instruction[1]
        opcode=instr[25:]
        if opcode=="0110011":      #instruction is r type
            rd=int("0b"+instr[20:25],0)
            rdval=bintoint(self.regfile[rd])
            rs1=int("0b"+instr[12:17],0)
            rs1val=bintoint(self.regfile[rs1])
            rs2=int("0b"+instr[7:12],0)
            rs2val=bintoint(self.regfile[rs2])
            funct3=instr[17:20]
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
                shiftval=int("0b"+(self.regfile[rs2])[27:],0)  #only las 5 bits of rs2 are considered as the shift value
                shiftres=int("0b"+self.regfile[rs1], 2) << shiftval  #shifting a binary number by n places is equivalent to multiplying its value by 2^n
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
                    shiftval=int("0b"+(self.regfile[rs2])[27:],0)  #only las 5 bits of rs2 are considered as the shift value
                    shiftres=int("0b"+self.regfile[rs1], 2) >> shiftval  #shifting a binary number by n places is equivalent to multiplying its value by 2^n
                    shiftresbin=actbin(shiftres,32)         #convert the value back to binary,restrict size to 32 bits
                    self.regfile[rd]=shiftresbin

                elif funct7=="0100000":   #sra-rigHt arithmetic shfit
                    shiftval=int("0b"+(self.regfile[rs2])[27:],0)  #only las 5 bits of rs2 are considered as the shift value
                    shiftres=bintoint(self.regfile[rs1]) >> shiftval  #shifting a binary number by n places is equivalent to multiplying its value by 2^n
                    shiftresbin=actbin(shiftres,32)
                    self.regfile[rd]=shiftresbin
                else:
                    print("Error, unidentified instruction")
            elif funct3=="110":     #bitwise OR
                res=rs1val|rs2val
                self.regfile[rd]=actbin(res,32)
            elif funct3=="111":    #bitwise AND
                res=rs1val&rs2val
                self.regfile[rd]=actbin(res,32)
            else:
                print("error: invalid instruction")   # in the top program if this is returned, halt the execution procedure okay??
                return
            pcbin=hextobin(self.pc)
            pcintnew=int("0b"+pcbin,0)+4
            self.pc=hexconv(actbin(pcintnew,32))
            self.regfile[0]="0"*32

        elif opcode=="0010011":
            imm=instr[0:12]
            rs1=int("0b"+instr[12:17],0)
            rs1val=bintoint(self.regfile[rs1])
            funct3=instr[17:20]
            rd=int("0b"+instr[20:25],0)
            immval=bintoint(imm)
            if funct3=="000":   #addi
                res=immval+rs1val
                resbin=actbin(res,32)
                self.regfile[rd]=resbin
            elif funct3=="010":   #slti-signed compare
                res=int(rs1val<immval)
                self.regfile[rd]=actbin(res,32)
            elif funct3=="011":   #sltiu-unsigned compare
                res=int(int("0b"+self.regfile[rs1],0)<int("0b"+actbin(bintoint(imm),32),0))
                self.regfile[rd]=actbin(res,32)
            elif funct3=="100":  #xori
                res=actbin(rs1val^immval,32)
                self.regfile[rd]=res
            elif funct3=="110":  #ori
                res=actbin(rs1val|immval,32)
                self.regfile[rd]=res
            elif funct3=="111":  #andi
                res=actbin(rs1val&immval,32)
                self.regfile[rd]=res
            elif funct3=="001": #slli- logical left shift by immediate amount
                shiftval=int("0b"+(imm)[7:],0)   
                shiftres=int("0b"+self.regfile[rs1], 2) << shiftval 
                shiftresbin=actbin(shiftres,32)         
                self.regfile[rd]=shiftresbin   #00000000011110010001100010010011
            elif funct3=="101":
                if imm[0:7]=="0000000":  #srli
                    shiftval=int("0b"+imm[7:],0)  
                    shiftres=int("0b"+self.regfile[rs1], 2) >> shiftval
                    shiftresbin=actbin(shiftres,32)         
                    self.regfile[rd]=shiftresbin
                elif imm[0:7]=="0100000":   #srai
                    shiftval=int("0b"+imm[7:],0)  #only las 5 bits of rs2 are considered as the shift value
                    shiftres=bintoint(self.regfile[rs1]) >> shiftval #shifting a binary number by n places is equivalent to multiplying its value by 2^n
                    shiftresbin=actbin(shiftres,32)
                    self.regfile[rd]=shiftresbin
                else:
                    print("invalid instruction this",funct3, imm[0:8] )
                    return
            else:
                print("invalid instruction")
                return
            pcbin=hextobin(self.pc)
            pcintnew=int("0b"+pcbin,0)+4
            self.pc=hexconv(actbin(pcintnew,32))
            self.regfile[0]="0"*32

        elif opcode=="0000011":
            imm=instr[0:12]
            rs1=int("0b"+instr[12:17],0)
            rs1val=bintoint(self.regfile[rs1])
            funct3=instr[17:20]
            rd=int("0b"+instr[20:25],0)
            immval=bintoint(imm)
            memadr=actbin(immval+rs1val,32)
            memadrhextemp=hexconv(memadr)
            memadrhex=convtoproper(memadrhextemp)
            memadrhexnext=hexconv(str(bin(4+int("0x"+memadrhex,0))[2::]))
            try:
                memory_access=self.datamem[memadrhex]
            except KeyError:
                memory_access="0"*32 
            try:
                memory_access_next=self.datamem[memadrhexnext]
            except KeyError:
                memory_access_next="0"*32            #need to use the address being acessed as well as teh next address to support misaligned accesses

            if funct3=="000" or funct3=="100":   #loadbyte or load byte unsigned
                if memadrhex in self.datamem:
                    if memadr[-2:]=="00":
                        self.regfile[rd]=memory_access[24:].zfill(32) if funct3=="100" else memory_access[24:][0]*24+memory_access[24:]
                    elif memadr[-2:]=="01":
                        self.regfile[rd]=memory_access[16:24].zfill(32) if funct3=="100" else memory_access[16:24][0]*24+memory_access[16:24]
                    elif memadr[-2:]=="10":
                        self.regfile[rd]=memory_access[8:16].zfill(32) if funct3=="100" else memory_access[8:16][0]*24+memory_access[8:16]
                    elif memadr[-2:]=="11":
                        self.regfile[rd]=memory_access[0:8].zfill(32) if funct3=="100" else memory_access[0:8][0]*24+memory_access[0:8]
                    else:
                        print("invalid address")
                        return
                else:
                    self.regfile[rd]="0".zfill(32)

            elif funct3=="001" or funct3=="101":   #load half word or load half word unsigned
                if memadrhex in self.datamem:
                    if memadr[-2:]=="00":
                        self.regfile[rd]=memory_access[16:].zfill(32)  if funct3=="101" else memory_access[16:][0]*16+memory_access[16:]
                    elif memadr[-2:]=="01":
                        self.regfile[rd]=memory_access[8:24].zfill(32) if funct3=="101" else memory_access[8:24][0]*16+memory_access[8:24]
                    elif memadr[-2:]=="10":
                        self.regfile[rd]=memory_access[0:16].zfill(32) if funct3=="101" else memory_access[0:16][0]*16+memory_access[0:16]
                    elif memadr[-2:]=="11":
                        self.regfile[rd]=(memory_access_next[24:]+memory_access[0:8]).zfill(32)  if funct3=="101" else (memory_access_next[24:][0]*16+memory_access[24:]+memory_access[0:8])
                    else:
                        print("Invalid address")
                        return
                else:
                    self.regfile[rd]="0".zfill(32)

            elif funct3=="010":   #Load word
                if memadrhex in self.datamem:
                    if memadr[-2:]=="00":
                        self.regfile[rd]=memory_access[0:].zfill(32)
                    elif memadr[-2:]=="01":
                        self.regfile[rd]=(memory_access_next[24:]+memory_access[0:24]).zfill(32)
                    elif memadr[-2:]=="10":
                        self.regfile[rd]=(memory_access_next[16:]+memory_access[0:16]).zfill(32)
                    elif memadr[-2:]=="11":
                        self.regfile[rd]=(memory_access_next[8:]+memory_access[0:8]).zfill(32)
                    else:
                        print("Invalid address")
                        return
                else:
                    self.regfile[rd]="0".zfill(32)
            pcbin=hextobin(self.pc)
            pcintnew=int("0b"+pcbin,0)+4
            self.pc=hexconv(actbin(pcintnew,32))
            self.regfile[0]="0"*32

        elif opcode=="0100011":   #store instructions
            rs1=int("0b"+instr[12:17],0)
            rs2=int("0b"+instr[7:12],0)
            immval=bintoint(instr[0:7]+instr[20:25])
            rs1val=bintoint(self.regfile[rs1])
            rs2val=bintoint(self.regfile[rs2])
            funct3=instr[17:20]
            memadr=actbin(immval+rs1val,32)
            memadrhextemp=hexconv(memadr)
            memadrhex=convtoproper(memadrhextemp)
            memadrhexnext=hexconv(str(bin(4+int("0x"+memadrhex,0))[2::]))
            try:
                memory_access=self.datamem[memadrhex]
            except KeyError:
                memory_access="0"*32
            try:
                memory_access_next=self.datamem[memadrhexnext]
            except KeyError:
                memory_access_next="0"*32  #need to use the address being acessed as well as teh next address to support misaligned accesses
            if funct3=="000":  #store byte
                if memadr[-2::]=="00":    #storing doesnt need an address exists check, casue we have to add the address on the go
                    self.datamem[memadrhex]=memory_access[0:24]+self.regfile[rs2][24:]
                elif memadr[-2:]=="01":
                    self.datamem[memadrhex]=memory_access[0:16]+self.regfile[rs2][24:]+memory_access[24:]
                elif memadr[-2:]=="10":
                    self.datamem[memadrhex]=memory_access[0:8]+self.regfile[rs2][24:]+memory_access[16:]
                elif memadr[-2:]=="11":
                    self.datamem[memadrhex]=self.regfile[rs2][24:]+memory_access[8:]
                else:
                    print('Invalid address')
                    return
                
            elif funct3=="001":  #store half word
                if memadr[-2:]=="00":
                    self.datamem[memadrhex]=memory_access[0:16]+self.regfile[rs2][16:]
                elif memadr[-2:]=="01":
                    self.datamem[memadrhex]=memory_access[0:8]+self.regfile[rs2][16:]+memory_access[24:]
                elif memadr[-2:]=="10":
                    self.datamem[memadrhex]=self.regfile[rs2][16:]+memory_access[16:]
                elif memadr[-2:]=="11":
                    self.datamem[memadrhex]=self.regfile[rs2][24:]+memory_access[8:]
                    self.datamem[memadrhexnext]=memory_access_next[0:24]+self.regfile[rs2][16:24]
                else:
                    print("Invalid address")
                    return
                
            elif funct3=="010":   #store word
                if memadr[-2:]=="00":
                    self.datamem[memadrhex]=self.regfile[rs2]
                elif memadr[-2:]=="01":
                    self.datamem[memadrhex]=self.regfile[rs2][8:]+memory_access[24:]
                    self.datamem[memadrhexnext]=memory_access_next[0:24]+self.regfile[rs2][0:8]
                elif memadr[-2:]=="10":
                    self.datamem[memadrhex]=self.regfile[rs2][16:]+memory_access[16:]
                    self.datamem[memadrhexnext]=memory_access_next[0:16]+self.regfile[rs2][0:16]
                elif memadr[-2:]=="11":
                    self.datamem[memadrhex]=self.regfile[rs2][24:]+memory_access[8:]
                    self.datamem[memadrhexnext]=memory_access_next[0:8]+self.regfile[rs2][0:24]
                else:
                    print("Invalid address")
                    return   
            pcbin=hextobin(self.pc)
            pcintnew=int("0b"+pcbin,0)+4
            self.pc=hexconv(actbin(pcintnew,32))  
            self.regfile[0]="0"*32           

        elif opcode=="1100011":
            rs1=int("0b"+instr[12:17],0)
            rs2=int("0b"+instr[7:12],0)
            funct3=instr[17:20]
            immval=bintoint(instr[0]+instr[24]+instr[1:7]+instr[20:24]+"0")     
            rs1val=bintoint(self.regfile[rs1])
            rs2val=bintoint(self.regfile[rs2])
            targetint=bintoint(hextobin(self.pc))+immval  #pc+immediate value
            targethex=hexconv(actbin(targetint,32))
            if funct3=="000" and rs1val==rs2val:
                self.pc=targethex
            elif funct3=="001" and rs1val!=rs2val:
                self.pc=targethex
            elif funct3=="100" and rs1val<rs2val:
                self.pc=targethex
            elif funct3=="101" and rs1val>=rs2val:
                self.pc=targethex
            elif funct3=="110" and int("0b"+self.regfile[rs1],0)<int("0b"+self.regfile[rs2],0):
                self.pc=targethex
            elif funct3=="111" and int("0b"+self.regfile[rs1],0)>=int("0b"+self.regfile[rs2],0):
                self.pc=targethex
            else:
                pcbin=hextobin(self.pc)
                pcintnew=int("0b"+pcbin,0)+4
                self.pc=hexconv(actbin(pcintnew,32))
            self.regfile[0]="0"*32

        elif opcode=="1100111":    #JALR
            rs1=int("0b"+instr[12:17],0)
            rs1val=bintoint(self.regfile[rs1])
            funct3=instr[17:20]
            rd=int("0b"+instr[20:25],0)
            immval=bintoint(instr[0:12])  
            pcbin=hextobin(self.pc)
            self.regfile[rd]=actbin(int("0b"+pcbin,0)+4,32)
            targetint=rs1val+immval  #pc+immediate value
            targethex=hexconv(actbin(targetint,32)[0:31]+"0")
            if bintoint(hextobin(targethex))%4!=0:
                print("invalid jump address")
                return
            self.pc=targethex    #change pc to jump value
            self.regfile[0]="0"*32

        elif opcode=="0110111":   #LUI
            imm=instr[0:20]
            rd=int("0b"+instr[20:25],0)
            self.regfile[rd]=imm+"0"*12
            pcbin=hextobin(self.pc)
            pcintnew=int("0b"+pcbin,0)+4
            self.pc=hexconv(actbin(pcintnew,32))
            self.regfile[0]="0"*32

        elif opcode=="0010111":   #AUIPC
            imm=instr[0:20]
            rd=int("0b"+instr[20:25],0)
            self.regfile[rd]=actbin(bintoint(imm+"0"*12)+bintoint(hextobin(self.pc)),32)
            pcintnew=int("0b"+hextobin(self.pc),0)+4
            self.pc=hexconv(actbin(pcintnew,32))
            self.regfile[0]="0"*32

        elif opcode=="1101111":  #JAL
            imm=instr[0]+instr[12:20]+instr[11]+instr[1:11]+"0"
            rd=int("0b"+instr[20:25],0)
            targetpc=actbin(bintoint(imm[0]*12+imm)+bintoint(hextobin(self.pc)),32)
            pcintnew=int("0b"+hextobin(self.pc),0)+4
            if bintoint(hextobin(targetpc))%4!=0:
                print("Invalid jump address")
                return
            self.regfile[rd]=actbin(pcintnew,32)
            self.pc=hexconv(targetpc)
            self.regfile[0]="0"*32
        
        else:
            print("invalid opcode")
            return

            





            






