import re
class code_splitter:
    def __init__(self):
        pass
    def split(self,code):
        s=code
        instructions=s.split("\n")  #label address is the adddress of the instruction after it
        instrandaddress=[]          #this method returns a list of lists containing every instructions, its address and whether its a label or not
        count=0
        for i in range(len(instructions)):
            c=instructions[i].split("#")    #removing comments
            current=c[0]
            if current.isspace() or current=="":                 #handling lines with only a comment
                continue
            if ":" in current:
                if (re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*:', current.strip())):
                    if ":" not in instructions[i+1]:                    #for handling multiple labels sandwiched together
                        instrandaddress.append(["0x"+str(hex(count)[2:].zfill(8)),"label",current])
                        count+=4                              #labels currently contain address of previous instruction, adjust the code so that their address is the address of teh succeeding instruction
                    else:
                        instrandaddress.append(["0x"+str(hex(count)[2:].zfill(8)),"label",current])
                else:
                    print("Invalid Label",instructions[i])
            else:
                instrandaddress.append(["0x"+str(hex(count)[2:].zfill(8)),current])
                count+=4
        return instrandaddress     

codesplit=code_splitter()
code="ADD x6,x5,x7 \n root: \n root2 \n SUB x5,x6,x7 \n ADDI x54,x3,12"
l=codesplit.split(code) 
print(l)