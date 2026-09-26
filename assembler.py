import re
class Assembler:
    def __init__(self,instrandaddr):    #assembler class holds the label table for the first pass
        self.instrandaddr=instrandaddr    #it is responsible for converting individual lines into machine code
        self.label_table={}   
        self.machinecode=[]  
        self.labels=[]           #and for identifying and storing label positions
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
        self.luti={"ADDI":  ["000", "0010011"],
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
                   "JALR":  ["000", "1100111"]}
        self.lutb={"BEQ":  ["000", "1100011"],
                   "BNE":  ["001", "1100011"],
                   "BLT":  ["100", "1100011"],
                   "BGE":  ["101", "1100011"],
                   "BLTU": ["110", "1100011"],
                   "BGEU": ["111", "1100011"]}
        self.lutj={"JAL": ["1101111"]}
        self.luts={"SB": ["000", "0100011"],
                   "SH": ["001", "0100011"],
                   "SW": ["010", "0100011"]}
        self.lutu={"LUI":   ["0110111"],
                   "AUIPC": ["0010111"]}

    def organise_label(self):
        for i in self.instrandaddr:
            if i[1]=="label":
                self.label_table[i[2]]=i[0]+0x00000004
    def assemble(self):        #instruction here is a single element from the instr and addr list [count,instr,type]
        code=self.instrandaddr
        for i in code:
            type=i[2]        
            if type=="r":
                self.machinecode.append(self.assemble_r_type(i))    #first pass can be managed by the code line splitter
            elif type=="i":                                 #itll assign an instruction address to each line as well
                 self.machinecode.append(self.assemble_i_type(i))    #it then calls the assembler class instance and store each label with its address in the label table
            elif type=="u":
                 self.machinecode.append(self.assemble_u_type(i))     
            elif type=="j":
                 self.machinecode.append(self.assemble_j_type(i))
            elif type=="b":
                 self.machinecode.append(self.assemble_b_type(i))
            elif type=="s":
                 self.machinecode.append(self.assemble_s_type(i))
            else:
                return "Error: unknown instruction type"
    def type_identify(self):
        r=["ADD","SUB","SLL","SLT","SLTU","XOR","SRL","SRA","OR","AND"]
        i=["JALR" ,"LB" ,"LH" ,"LW" ,"LBU" ,"LHU" ,"ADDI" ,"SLTI" ,"SLTIU" ,"XORI","ORI" ,"ANDI" ,"SLLI" ,"SRLI" ,"SRAI"]
        u=["LUI","AUIPC"]
        s=["SB","SH","SW"]
        b=["BEQ" ,"BNE" ,"BLT" ,"BGE" ,"BLTU" ,"BGEU "]
        j=["JAL"]
        for k in range(len(self.instrandaddr)):
            i=self.instrandaddr[k]
            if i[1]!="label":
                inst=i[1]
                instruction=inst.strip()   #remove whitespace from instructions
                mnemonic=""
                x=0
                while instruction[x].isalpha():        #stops at first space
                    mnemonic+=instruction[x].upper() 
                    x+=1                        #extract the instruction like which operation
                if mnemonic in r:
                    self.instrandaddr[k].append("r")
                elif mnemonic in j:
                    self.instrandaddr[k].append("j")
                elif mnemonic in u:
                    self.instrandaddr[k].append("u")
                elif mnemonic in s:
                    self.instrandaddr[k].append("s")
                elif mnemonic in i:
                    self.instrandaddr[k].append("i")
                elif mnemonic in b:
                    self.instrandaddr[k].append("b")
                else:
                    print("invalid instruction",i)
                    return
            else:
                self.labels.append(i)
                self.instrandaddr.remove(i)
                

    def assemble_r_type(self,instruction):
        line=instruction[1]
        y = re.sub(r'\s*,\s*', ',', line)
        y = re.sub(r'\s+', ' ', y).strip()
        if len(y.split(" "))!=2:
            print("Invalid R-type instruction")
            return
        if (line.count("x")+line.count("X")!=3) or (line.count(',')!=2):   #all r types have 3 x's in them
            print("invalid R-type instruction",line)
        else:
            properformat=""           #properformat contains the entire instruction in all caps, without spaces or commas
            for i in line:
                if i.isalpha():
                    properformat+=i.upper()
                elif i.isdigit():
                    properformat+=str(i)
                else:
                    continue
            properformat_list=properformat.split("X")#this list contains the mnemonic, and the register numbers
            try:
                properformat_list[1:] = [int(i) for i in properformat_list[1:]]
            except ValueError:
                print("Invalid R-type instruction",instruction)
                return
            if properformat_list[0] not in self.lutr:
                print("Invalid r type instruction",instruction)
            else:             
                if all(0 <= i <= 31 for i in properformat_list[1:]):   #check whether register numbers are numbers itself and if theyre valid or not its confirmed that the word add is in there.
                    machine_code=self.lutr[properformat_list[0]][0]+str(bin(properformat_list[3])[2:]).zfill(5)+str(bin(properformat_list[2])[2:]).zfill(5)+self.lutr[properformat_list[0]][1]+str(bin(properformat_list[1])[2:]).zfill(5)+self.lutr[properformat_list[0]][2]   #r type instruction converted to machine code
                    self.machinecode.append([instruction[0],machine_code])    #add instruction address and machine code version of instruction to the machine code storage
                else:
                    print("Invalid R -type instruction",instruction)

    def assemble_i_type(self,instruction): 
        line=instruction[1] 
        y = re.sub(r'\s*,\s*', ',', line)
        y = re.sub(r'\s+', ' ', y).strip()
        if len(y.split(" "))!=2:
            print("Invalid I-type instruction")
            return                                #Register aliases defined by the RISC-V ABI (e.g. sp, ra, a0) are not supported; registers must be specified using the x0–x31 notation. Stack-specific pseudo-instructions and stack management are outside the scope of the assembler.
        properformattemp=""                                      #
        for i in instruction:
            if i.isalpha():
                properformattemp+=i.upper()
            elif i.isdigit():
                properformattemp+=str(i)
            elif i in [',','(',")",'-']:
                properformattemp+=i
            else:
                continue             #since hex immediates will be supported, the x from the hex string should be replace with a temporary 'h' before the validity tests
        z=0
        properformat=""
        for i in range(len(properformattemp)):
            if properformattemp[i]=="X":
                if properformattemp[i-1]=="0":
                    properformat+="h"
                else:
                    properformat+=properformattemp[i]
            else:
                properformat+=properformattemp[i]

            

        if properformat.count("X")!=2:
            print("Invalid I-type instruction", instruction)  #checking if it has mentioned two registers
        else:
            properformat_list=properformat.split('X')
            if properformat_list[0] not in self.luti:       #checking if the instruction is valid to begin with
                print("Invalid I-type instruction", instruction)
            else:
                if properformat_list[0] in ["ADDI","SLTI","SLTIU","XORI","ORI","ANDI"] and properformat.count(",")==2:  #instruction wise handling within i types for instructions with similar formatting
                    temp=properformat_list[2]
                    properformat_list.pop()
                    properformat_list.extend(temp.split(","))
                    try:
                        properformat_list[1]=int(properformat_list[1].strip(','))    #removing extra comma from second register value
                        properformat_list[2]=int(properformat_list[2])
                        properformat_list[3]=int(properformat_list[3].replace("h","x"),0)    #converting back to proper hex
                    except ValueError:
                        print("Invalid I-type instruction",instruction)      #in case int conversion fails
                        return
                    if all(0<=i<=31 for i in properformat_list[1:3] and -2048<=properformat[3]<=2047):    #checking register file as well as immediate limits
                        machine_code=str(bin(properformat_list[3])[2:]).zfill(12)+str(bin(properformat_list[2])[2:]).zfill(5)+self.luti[properformat_list[0]][2]+str(bin(properformat_list[1])[2:]).zfill(5)+self.luti[properformat_list[0]][2]
                        self.machinecode.append([instruction[0],machine_code]) 
                    else:
                        print("Invalid I-type instruction",instruction)
                elif properformat_list[0] in ["LB","LH","LW","LBU","LHU","JALR"] and properformat.count(",")==1:
                    temp1=properformat_list[2]
                    temp2=properformat_list[1]
                    properformat_list.extend(temp2.strip("(").split(","))
                    properformat_list.append(temp1.strip("("))    #list is of the form ["INSTRUCTION","RD","offset","rs1"]
                    try:
                        properformat_list[2]=int(properformat_list[3].replace("h","x"),0)
                        properformat_list[1]=int(properformat_list[1])
                        properformat_list[3]=int(properformat_list[3])
                    except ValueError:
                        print("Invalid I-type instruction")
                    if all(0<=properformat_list[1]<=31 and 0<=properformat_list[3]<=31 and -2048<=properformat_list[2]<=2047):
                        machine_code=str(bin(properformat_list[2])[2:]).zfill(12)+str(bin(properformat_list[3])[2:]).zfill(5)+self.luti[properformat_list[0]][2]+str(bin(properformat_list[1])[2:]).zfill(5)+self.luti[properformat_list[0]][2]
                        self.machinecode.append([instruction[0],machine_code]) 
                    else:
                        print('Invalid I-type instruction',instruction)

    def assemble_b_type()





        


            
                  
                




        


        





    