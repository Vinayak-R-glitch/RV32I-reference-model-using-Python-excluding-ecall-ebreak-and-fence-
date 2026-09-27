class rv32i_core:
    def __init__(self,pc):
        self.pc=pc
        self.regfile=[]
        self.datamem={}
    