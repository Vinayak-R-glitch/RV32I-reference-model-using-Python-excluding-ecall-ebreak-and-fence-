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
    def assemble(self,instruction):        #instruction here is a single element from the instr and addr list [count,instr,type]
        type=instruction[2]        
        if type=="r":
            return self.assemble_r_type(instruction)    #first pass can be managed by the code line splitter
        elif type=="i":                                 #itll assign an instruction address to each line as well
            return self.assemble_i_type(instruction)    #it then calls the assembler class instance and store each label with its address in the label table
        elif type=="u":
            return self.assemble_u_type(instruction)     
        elif type=="j":
            return self.assemble_j_type(instruction)
        elif type=="b":
            return self.assemble_b_type(instruction)
        elif type=="s":
            return self.assemble_s_type(instruction)
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
                if mnemonic in j:
                    self.instrandaddr[k].append("j")
                if mnemonic in u:
                    self.instrandaddr[k].append("u")
                if mnemonic in s:
                    self.instrandaddr[k].append("s")
                if mnemonic in i:
                    self.instrandaddr[k].append("i")
                if mnemonic in b:
                    self.instrandaddr[k].append("b")
                else:
                    print("invalid instruction",i)
                    return
            else:
                self.labels.append(i)
                self.instrandaddr.remove(i)
                

    def assemble_r_type(self,instruction):
        line=instruction[1]
        if line.count("x")+line.count("X")!=3:   #all r types have 3 x's in them
            print("invalid R-type instruction",line)
            return
        else:
            properformat=""           #properformat contains the entire instruction in all caps, without spaces or commas
            for i in line:
                if i.isalpha():
                    properformat+=i.upper()
                elif i.isdigit():
                    properformat+=str(i)
                else:
                    continue
            properformat_list=properformat.split("X")  #this list contains the mnemonic, and the register numbers

            
                    
            
            
        
        
        
        
        
class code_splitter:
    def __init__(self,code):
        self.code=code
    def split(self):
        s=self.code
        instructions=s.split("\n")  #label address is the adddress of the instruction after it
        instrandaddress=[]          #this method returns a list of lists containing every instructions, its address and whether its a label or not
        count=0x00000000
        for i in range(len(instructions)):
            c=instructions[i].split("#")    #removing comments
            current=c[0]
            if current.isspace() or current=="":                 #handling lines with only a comment
                continue
            if ":" in current:
                if ":" not in instructions[i+1]:                    #for handling multiple labels sandwiched together
                    instrandaddress.append([count,"label",current])
                    count+=0x00000004                                  #labels currently contain address of previous instruction, adjust the code so that their address is the address of teh succeeding instruction
                else:
                    instrandaddress.append([count,"label",current])

            else:
                instrandaddress.append([count,current])
                count+=0x00000004
        return instrandaddress                      #this  is used while initialising class assembler
                





        


        





    