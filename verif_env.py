import cpu_model
import assembler 
import code_splitter

CORE=cpu_model.rv32i_core()
SPLITTER=code_splitter.code_splitter()

def step_one(i):
    CORE.decode_execute(i)
    display_datamem()
    display_regfile()

def exec_all(machinecode):   #executes all leftover instructions starting from current state
    currentpc=CORE.pc
    for i in range(len(machinecode)):
        if machinecode[i][0]==currentpc:
            machinecode_=machinecode[i::]
            break
        else:
            continue
    for i in machinecode_:
        CORE.decode_execute(i)
    display_regfile()
    display_datamem()

def display_regfile():
    print("\n========== REGISTER FILE ==========")

    for i in range(0, 32, 4):
        for j in range(i, i + 4):
            value =cpu_model.hexconv(CORE.regfile[j]).zfill(8)
            print(f"x{j:<2} = 0x{value}", end="    ")
        print()

    print("===================================")

def display_datamem():
    print("\n========== DATA MEMORY ==========")

    for address in dict(sorted(CORE.datamem.items(), key=lambda item: int(item[0], 16))):
        value = cpu_model.hexconv(CORE.datamem[address]).zfill(8)
        print(f"Address: {address} | Value: 0b{value}")

    print("================================")

def main():
    path=input("Enter Assembly text file path") 
    with open(path,"r") as file:
        assembly_code=file.read()
    instrandaddr=SPLITTER.split(assembly_code)
    """ print(instrandaddr) """
    ASSEMBLER=assembler.Assembler(instrandaddr)
    ASSEMBLER.type_identify()
    """ print(ASSEMBLER.instrandaddr)  """
    ASSEMBLER.assemble()
    machinecode=ASSEMBLER.machinecode
    """ print(ASSEMBLER.machinecode) """
    while True:
        i=0
        print("\n===== RISC-V INTERPRETER =====")
        print("1. Execute one instruction")
        print("2. Execute all instructions and display final state")
        print("3. Execute and trace one instruction")
        print("4. Display Register file")
        print("5. Display data memory")
        print("6. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            CORE.decode_execute(machinecode[i])
            i+=1
        elif choice == "2":
            for j in machinecode[i::]:
                CORE.decode_execute(j)
                i=len(machinecode)
        elif choice == "3":
            step_one(machinecode[i])
            i+=1
        elif choice == "4":
            display_regfile()
        elif choice == "5":
            display_datamem()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Try again.")

main()  

