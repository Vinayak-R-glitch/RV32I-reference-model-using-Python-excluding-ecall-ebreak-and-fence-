import re
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
    return a[-8:]

def hextobin(hexstring):
    hex_only=hexstring[2::]
    binfinal=""
    for i in hex_only:
        hexbit=str(bin(int(i,16))[2::]).zfill(4)
        binfinal+=hexbit
    return binfinal

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


class Assembler:
    def __init__(self,instrandaddr):    #assembler class holds the label table for the first pass
        self.instrandaddr=instrandaddr    #it is responsible for converting individual lines into machine code
        self.label_table={}   
        self.machinecode=[]  
        self.lutr={"ADD":  ["0000000", "000", "0110011"],
                   "SUB":  ["0100000", "000", "0110011"],
                   "SLL":  ["0000000", "001", "0110011"],
                   "SLT":  ["0000000", "010", "0110011"],
                   "SLTU": ["0000000", "011", "0110011"],
                   "XOR":  ["0000000", "100", "0110011"],
                   "SRL":  ["0000000", "101", "0110011"],
                   "SRA":  ["0100000", "101", "0110011"],
                   "OR":   ["0000000", "110", "0110011"],
                   "AND":  ["0000000", "111", "0110011"]}
        self.luti_s={"ADDI":  ["000", "0010011"],
                   "SLTI":  ["010", "0010011"],
                   "SLTIU": ["011", "0010011"],
                   "XORI":  ["100", "0010011"],
                   "ORI":   ["110", "0010011"],
                   "ANDI":  ["111", "0010011"],
                   "SLLI":  ["001", "0010011"],
                   "SRLI":  ["101", "0010011"],
                   "SRAI":  ["101", "0010011"],
                   "LB":    ["000", "0000011"],
                   "LH":    ["001", "0000011"],
                   "LW":    ["010", "0000011"],
                   "LBU":   ["100", "0000011"],
                   "LHU":   ["101", "0000011"],
                   "JALR":  ["000", "1100111"],
                   "SB": ["000", "0100011"],
                   "SH": ["001", "0100011"],
                   "SW": ["010", "0100011"]}
        self.lutb={"BEQ":  ["000", "1100011"],
                   "BNE":  ["001", "1100011"],
                   "BLT":  ["100", "1100011"],
                   "BGE":  ["101", "1100011"],
                   "BLTU": ["110", "1100011"],
                   "BGEU": ["111", "1100011"]}
        self.lutj={"JAL": ["1101111"]}
        self.lutu={"LUI":   ["0110111"],
                   "AUIPC": ["0010111"]}
 
    def assemble(self):        #instruction here is a single element from the instr and addr list [count,instr,type]
        for i in self.instrandaddr:
            line=i[1]
            y = re.sub(r'\s*,\s*', ',', line)
            y = re.sub(r'\s+', ' ', y).strip()
            if len(y.split(" "))!=2:
                print("Invalid instruction first")
                return
            for z in y:
                if (z not in ["(",")",",","-"] and not z.isalpha() and not z.isdigit() and not z.isspace()):
                    print("Invalid instruction second",z) 
                    return 
            type=i[2]        
            if type=="r":
                self.machinecode.append(self.assemble_r_type(i))    #first pass can be managed by the code line splitter
            elif type=="i" or type=="s":                                 #itll assign an instruction address to each line as well
                 self.machinecode.append(self.assemble_i_s_type(i))    #it then calls the assembler class instance and store each label with its address in the label table
            elif type=="u":
                 self.machinecode.append(self.assemble_u_type(i))     
            elif type=="j":
                 self.machinecode.append(self.assemble_j_type(i))
            elif type=="b":
                 self.machinecode.append(self.assemble_b_type(i))
            else:
                return "Error: unknown instruction type"
        for i in self.machinecode:    #'None' keeps getting added between every instruction, idk why its happening so this is to remove that
            if i is None:
                self.machinecode.remove(i)
    def type_identify(self):               #this function both identifies the type of every instruction and adds labels to the label table
        r=["ADD","SUB","SLL","SLT","SLTU","XOR","SRL","SRA","OR","AND"]
        i=["JALR" ,"LB" ,"LH" ,"LW" ,"LBU" ,"LHU" ,"ADDI" ,"SLTI" ,"SLTIU" ,"XORI","ORI" ,"ANDI" ,"SLLI" ,"SRLI" ,"SRAI"]
        u=["LUI","AUIPC"]
        s=["SB","SH","SW"]
        b=["BEQ" ,"BNE" ,"BLT" ,"BGE" ,"BLTU" ,"BGEU"]
        j=["JAL"]
        for k in range(len(self.instrandaddr)):
            a=self.instrandaddr[k]
            if a[1]!="label":
                inst=a[1]
                instruction=inst.strip()   #remove whitespace from instructions
                mnemonic=""
                x=0
                while instruction[x].isalpha():     
                    if instruction[x] in["x",'X']:
                        if instruction[x+1] in ['o','O']:   #stops at first space
                            mnemonic+=instruction[x].upper() 
                        else:
                            break
                    else:
                        mnemonic+=instruction[x].upper()
                    x+=1                        #extract the instruction like which operation
                if mnemonic in r:
                    if mnemonic=="XOR":
                        self.instrandaddr[k].extend("r","xor")
                    else:
                        self.instrandaddr[k].append('r')
                elif mnemonic in j:
                    self.instrandaddr[k].append("j")
                elif mnemonic in u:
                    self.instrandaddr[k].append("u")
                elif mnemonic in s:
                    self.instrandaddr[k].append("s")
                elif mnemonic in i:
                    if mnemonic=="XORI":
                        self.instrandaddr[k].extend("i","xori")
                    else:
                        self.instrandaddr[k].append("i")
                elif mnemonic in b:
                    self.instrandaddr[k].append("b")
                else:
                    print("invalid instruction here",mnemonic)
                    return
            else:
                z=""
                for j in i[2]:
                    if j.isalpha:
                        z+=j.upper
                self.label_table[z]=i[0]
                self.instrandaddr.remove(i)
                

    def assemble_r_type(self,instruction):
        line=instruction[1]
        if (line.count("x")+line.count("X")!=3) or (line.count(',')!=2):   #all r types have 3 x's in them
            print("invalid R-type instruction ",line)
        else:
            properformat=""           #properformat contains the entire instruction in all caps, without spaces or commas
            for i in line:
                if i.isalpha():
                    properformat+=i.upper()
                elif i.isdigit():
                    properformat+=str(i)
                elif i in [',','(',")",'-']:
                    properformat+=i
                else:
                    continue
            properformat_list=properformat.split("X")#this list contains the mnemonic, and the register numbers
            properformat_list[2]=properformat_list[2].strip(", ")
            properformat_list[1]=properformat_list[1].strip(", ")
            try:
                properformat_list[1:] = [int(i) for i in properformat_list[1:]]
            except ValueError:
                print("Invalid R-type instruction ",instruction)
                return
            if properformat_list[0] not in self.lutr:
                print("Invalid r type instruction",instruction)
            else:             
                if all(0 <= i <= 31 for i in properformat_list[1:]):   #check whether register numbers are numbers itself and if theyre valid or not its confirmed that the word add is in there.
                    machine_code=self.lutr[properformat_list[0]][0]+str(bin(properformat_list[3])[2:]).zfill(5)+str(bin(properformat_list[2])[2:]).zfill(5)+self.lutr[properformat_list[0]][1]+str(bin(properformat_list[1])[2:]).zfill(5)+self.lutr[properformat_list[0]][2]   #r type instruction converted to machine code
                    self.machinecode.append([instruction[0],machine_code])    #add instruction address and machine code version of instruction to the machine code storage
                else:
                    print("Invalid R -type instruction",instruction)

    def assemble_i_s_type(self,instruction):   
        line=instruction[1]                            #Register aliases defined by the RISC-V ABI (e.g. sp, ra, a0) are not supported; registers must be specified using the x0–x31 notation. Stack-specific pseudo-instructions and stack management are outside the scope of the assembler.
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

            

        if properformat.count("X")!=2:
            print("Invalid I-type instruction this", instruction)  #checking if it has mentioned two registers
        else:
            properformat_list=properformat.split('X')
            if properformat_list[0] not in self.luti_s:       #checking if the instruction is valid to begin with
                print("Invalid I-type instruction", instruction)
            else:
                if properformat_list[0] in ["ADDI","SLTI","SLTIU","XORI","ORI","ANDI","SLLI","SRAI","SRLI"] and properformat.count(",")==2:  #instruction wise handling within i types for instructions with similar formatting
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
                        print("Invalid I-type instruction",instruction)      #in case int conversion fails
                        return
                    if z==1:
                        if all(0<=i<=31 for i in properformat_list[1:3]) and -2048<=bintoint(hextobin(properformat_list[3]))<=2047:    #checking register file as well as immediate limits
                            machine_code=actbin(int(properformat_list[3],0),12)+str(bin(properformat_list[2])[2:]).zfill(5)+self.luti_s[properformat_list[0]][0]+str(bin(properformat_list[1])[2:]).zfill(5)+self.luti_s[properformat_list[0]][1]
                            self.machinecode.append([instruction[0],machine_code]) 
                        else:
                            print("Invalid I-type instruction",instruction)
                    else:
                        if all(0<=i<=31 for i in properformat_list[1:3]) and -2048<=(properformat_list[3])<=2047:    #checking register file as well as immediate limits
                            machine_code=actbin(properformat_list[3],12)+str(bin(properformat_list[2])[2:]).zfill(5)+self.luti_s[properformat_list[0]][0]+str(bin(properformat_list[1])[2:]).zfill(5)+self.luti_s[properformat_list[0]][1]
                            self.machinecode.append([instruction[0],machine_code]) 
                        else:
                            print("Invalid I-type instruction",instruction)
                elif properformat_list[0] in ["LB","LH","LW","LBU","LHU","JALR","SW","SB","SH"] and properformat.count(",")==1:
                    temp1=properformat_list[2]
                    temp2=properformat_list[1]
                    properformat_list.remove(temp1)
                    properformat_list.remove(temp2)
                    properformat_list.extend(temp2.strip("(").split(","))
                    properformat_list.append(temp1.strip(")"))    #list is of the form ["INSTRUCTION","RD","offset","rs1"]
                    try:
                        if z==1:
                            properformat_list[2]=int(properformat_list[3].replace("h","x"),0)
                        else:
                            properformat_list[2]=int(properformat_list[2])
                        properformat_list[1]=int(properformat_list[1])
                        properformat_list[3]=int(properformat_list[3])
                    except ValueError:
                        print("Invalid I/S-type instruction ")
                    if z==1:
                        if (0<=properformat_list[1]<=31 and 0<=properformat_list[3]<=31) and -2048<=bintoint(hextobin((properformat_list[2])))<=2047:
                            if properformat_list[0] in ["LB","LH","LW","LBU","LHU","JALR"]:
                                machine_code=actbin(int(properformat_list[2],0),12)+str(bin(properformat_list[3])[2:]).zfill(5)+self.luti_s[properformat_list[0]][0]+str(bin(properformat_list[1])[2:]).zfill(5)+self.luti_s[properformat_list[0]][1]
                            else:
                                machine_code=actbin(int(properformat_list[2],0),12)[0:7]+str(bin(properformat_list[1])[2:]).zfill(5)+str(bin(properformat_list[3])[2:]).zfill(5)+self.luti_s[properformat_list[0]][0]+actbin(int(properformat_list[2],0),12)[7:]+self.luti_s[properformat_list[0]][1]
                            self.machinecode.append([instruction[0],machine_code]) 
                        else:
                            print('Invalid I/S-type instruction',instruction)
                    else:
                        if (0<=properformat_list[1]<=31 and 0<=properformat_list[3]<=31) and -2048<=(properformat_list[2])<=2047:
                            if properformat_list[0] in ["LB","LH","LW","LBU","LHU","JALR"]:
                                machine_code=actbin(properformat_list[2],12)+str(bin(properformat_list[3])[2:]).zfill(5)+self.luti_s[properformat_list[0]][0]+str(bin(properformat_list[1])[2:]).zfill(5)+self.luti_s[properformat_list[0]][1]
                            else:
                                machine_code=actbin(properformat_list[2],12)[0:7]+str(bin(properformat_list[1])[2:]).zfill(5)+str(bin(properformat_list[3])[2:]).zfill(5)+self.luti_s[properformat_list[0]][0]+actbin(properformat_list[2],12)[7:]+self.luti_s[properformat_list[0]][1]
                            self.machinecode.append([instruction[0],machine_code]) 
                        else:
                            print('Invalid I/S-type instruction',instruction)
                else:
                    print("Invalid I/S-type instruction",instruction)

    def assemble_b_type(self,instruction):
        line=instruction[1]                            #Register aliases defined by the RISC-V ABI (e.g. sp, ra, a0) are not supported; registers must be specified using the x0–x31 notation. Stack-specific pseudo-instructions and stack management are outside the scope of the assembler.
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
        if properformat.count("X")!=2:
            print("Invalid B-type instruction", instruction)  #checking if it has mentioned two registers
        else:
            properformat_list=properformat.split('X')
            if properformat_list[0] not in self.lutb:       #checking if the instruction is valid to begin with
                print("Invalid B-type instruction", instruction, "Unidentified instruction")
            else:
                if properformat.count(",")==2:
                    properformat_list[1]=properformat_list[1].strip(",")
                    temp=properformat_list[2]
                    properformat_list.pop()
                    properformat_list.extend(temp.split(","))
                    try:
                        if z==1:
                            properformat_list[3]=int(properformat_list[3].replace("h","x"),0)
                        else:
                
                            if properformat_list[3][0].isalpha() or properformat_list[3][0]=="_":
                                pass
                            else:
                                properformat_list[3]=int(properformat_list[3])
                        properformat_list[1]=int(properformat_list[1])
                        properformat_list[2]=int(properformat_list[2])
                    except ValueError:
                        print("Invalid B-type instruction",instruction,"Invalid register numbering")
                    if not isinstance(properformat_list[3],int):
                        if properformat_list[3][0].isalpha() or properformat_list[3][0]=="_":
                            if all(0<=i<=31 for i in properformat_list[1:3]) and properformat_list[3] in self.label_table:
                                strinstad=self.label_table[properformat_list[3]]
                                if -4096<=bintoint(hextobin((instruction[0])))-bintoint(hextobin(strinstad))<=4094:
                                    numbi=bintoint(hextobin((instruction[0])))-bintoint(hextobin((strinstad)))
                                    numbiact=actbin(numbi,13)[0:12]
                                    machine_code=numbiact[0]+numbiact[2:8]+str(bin(properformat_list[2])[2:]).zfill(5)+str(bin(properformat_list[1])[2:]).zfill(5)+self.lutb[properformat_list[0]][0]+numbiact[8:12]+numbiact[1]+self.lutb[properformat_list[0]][1]
                                    self.machinecode.append([instruction[0],machine_code])
                                else:
                                    print("Invalid B-type instruction",instruction,"Jump address out of range")
                                    return
                            else:
                                print("invalid b type instruction, invalid label")
                        else:
                            print("Invalid b type instruction")
                    else:
                        if all(0<=i<=31 for i in properformat_list[1:3]) and -4096<=properformat_list[3]<=4094 and properformat_list[3]%2==0:
                            numbiact=actbin(properformat_list[3],13)[0:12]  #remove the last bit, it is added back by the processor decoding unit, this is done to improve jump range
                            machine_code=numbiact[0]+numbiact[2:8]+str(bin(properformat_list[2])[2:]).zfill(5)+str(bin(properformat_list[1])[2:]).zfill(5)+self.lutb[properformat_list[0]][0]+numbiact[8:]+numbiact[1]+self.lutb[properformat_list[0]][1]
                            self.machinecode.append([instruction[0],machine_code])
                        else:
                            print("Invalid B-type instruction",instruction,"Jump address out of range")
                            return
                else:
                    print("Invalid B-type isntruction", instruction)

    def assemble_u_type(self,instruction):
        line=instruction[1]
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
        z=0
        for i in range(len(properformattemp)):
            if properformattemp[i]=="X":
                if properformattemp[i-1]=="0":
                    properformat+="h"
                    z=1
                else:
                    properformat+=properformattemp[i]
            else:
                properformat+=properformattemp[i]
        if properformat.count("X")!=1:
            print("Invalid U-type instruction this", instruction,properformat)
        else:
            properformat_list=properformat.split("X")
            if properformat_list[0] not in self.lutu:
                print("Invalid U-type instruction",instruction)
            else:
                if properformat.count(",")==1:
                    temp=properformat_list[1]
                    properformat_list.pop()
                    properformat_list.extend(temp.split(","))
                    try:
                        properformat_list[1]=int(properformat_list[1])
                        if z==1:
                            properformat_list[2]=properformat_list[2].replace("h","x")
                        else:
                            properformat_list[2]=int(properformat_list[2])
                    except ValueError:
                        print("Invalid U-type instruction ")
                        return
                    if z==1:
                        if(0<=properformat_list[1]<=31) and 0<=int(properformat_list[2],0)<=1048575:
                            machine_code=str(bin(int(properformat_list[2],0))[2:]).zfill(20)+str(bin(properformat_list[1])[2:]).zfill(5)+self.lutu[properformat_list[0]][0]
                            self.machinecode.append([instruction[0],machine_code])
                        else:
                            print("Invalid U-type instruction ")
                    else:
                        if(0<=properformat_list[1]<=31 and 0<=properformat_list[2]<=1048575):   #no negative immediates
                            machine_code=str(bin(properformat_list[2])[2:]).zfill(20)+str(bin(properformat_list[1])[2:]).zfill(5)+self.lutu[properformat_list[0]][0]
                            self.machinecode.append([instruction[0],machine_code])
                        else:
                            print("Invalid U-type instruction ")
                else:
                    print("Invalid u type instruction")

    def assemble_j_type(self,instruction):
        line=instruction[1]
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
        z=0
        for i in range(len(properformattemp)):
            if properformattemp[i]=="X":
                if properformattemp[i-1]=="0":
                    properformat+="h"
                    z=1
                else:
                    properformat+=properformattemp[i]
            else:
                properformat+=properformattemp[i]

        if properformat.count("X")!=1:
            print("Invalid J-type instruction", instruction)
        else:
            properformat_list=properformat.split('X')
            if properformat_list[0] not in self.lutj:       #checking if the instruction is valid to begin with
                print("Invalid J-type instruction", instruction, "Unidentified instruction")
            else:
                if properformat.count(",")==1:
                    temp=properformat_list[1]
                    properformat_list.pop()
                    properformat_list.extend(temp.split(","))
                    try:
                        properformat_list[1]=int(properformat_list[1])
                        if z==1:
                            properformat_list[2]=properformat_list[2].replace("h","x")
                            properformat_list[2]=int(properformat_list[2],0)
                        else:
                            
                            if properformat_list[2][0].isalpha() or properformat_list[2][0]=="_":
                                    pass
                            else:
                                properformat_list[2]=int(properformat_list[2])
                    except ValueError:
                        print("Invalid J-type instruction ", instruction)
                    
                    if not isinstance(properformat_list[2],int):
                        if properformat_list[2][0].isalpha() or properformat_list[2][0]=="_":
                            if all(0<=properformat_list[1]<=31) and properformat_list[2] in self.label_table:
                                strinstad=self.label_table[properformat_list[2]]
                                if -1048576<=bintoint(hextobin((instruction[0])))-bintoint(hextobin(strinstad))<=1048576:
                                    numbi=bintoint(hextobin((instruction[0])))-bintoint(hextobin((strinstad)))
                                    numbiact=actbin(numbi,21)[0:20]
                                    machine_code=numbiact[0]+numbiact[10:20]+numbiact[9]+numbiact[1:9]+str(bin(properformat_list[1])[2:]).zfill(5)+self.lutb[properformat_list[0]][0]
                                    self.machinecode.append([instruction[0],machine_code])
                                else:
                                    print("Invalid J-type instruction",instruction,"Jump address out of range")
                                    return
                            else:
                                print("invalid j type instruction, invalid label")
                        else:
                            print("Invalid j type instruction this")
                    else:
                        if 0<=properformat_list[1]<=31 and -1048576<=properformat_list[2]<=1048576 and properformat_list[2]%2==0:
                            numbiact=actbin(properformat_list[2],21)[0:20] #remove the last bit, it is added back by the processor decoding unit, this is done to improve jump range
                            machine_code=numbiact[0]+numbiact[10:20]+numbiact[9]+numbiact[1:9]+str(bin(properformat_list[1])[2:]).zfill(5)+self.lutj[properformat_list[0]][0]
                            self.machinecode.append([instruction[0],machine_code])
                        else:
                            print("Invalid j-type instruction",instruction,"Jump address out of range")
                            return
                else:
                    print("Invalid j-type isntruction", instruction)
                
        



        
        
        

        





        


            
                  
                




        


        





    