class rv32i_core:
    def __init__(self,pc,regfile,datamem):
        self.pc=pc
        self.regfile={}
        self.datamem=