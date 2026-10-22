import cpu_model
import assembler 
import code_splitter
global machinecode
machinecode={}
CORE=cpu_model.rv32i_core()
SPLITTER=code_splitter.code_splitter()

def step_one():
    instruction=machinecode["0x"+CORE.pc]
    CORE.decode_execute(instruction)
    display_datamem()
    display_regfile()

def exec_all():   #executes all leftover instructions starting from current state
    while "0x"+CORE.pc in machinecode:
        instruction=machinecode["0x"+CORE.pc]
        CORE.decode_execute(instruction)
    display_regfile()
    display_datamem()

def exec_one():
    instruction=machinecode["0x"+CORE.pc]
    CORE.decode_execute(instruction)
def display_regfile():
    print("\n========== REGISTER FILE ==========")

    for i in range(0, 32, 4):
        for j in range(i, i + 4):
            if j==0:
                print("x0 = ",cpu_model.hexconv(CORE.regfile[0]),end ="    ")
            else:
                value =cpu_model.hexconv(CORE.regfile[j]).zfill(8)
                print(f"x{j:<2} = 0x{value}", end="    ")
        print()

    print("===================================")

def display_datamem():
    print("\n========== DATA MEMORY ==========")

    for address in dict(sorted(CORE.datamem.items(), key=lambda item: int(item[0], 16))):
        value = cpu_model.hexconv(CORE.datamem[address]).zfill(8)
        print(f"Address: {address} | Value: 0x{value}")

    print("================================")

def main():
    path=input("Enter Assembly text file path")  
    with open(path,"r") as file:
        assembly_code=file.read()
    instrandaddr=SPLITTER.split(assembly_code)
    ASSEMBLER=assembler.Assembler(instrandaddr)
    ASSEMBLER.type_identify() 
    ASSEMBLER.assemble()
    for i in ASSEMBLER.machinecode:
        machinecode[i[0]]=i
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
            exec_one()
        elif choice == "2":
            exec_all()
        elif choice == "3":
            step_one()
        elif choice == "4":
            display_regfile()
        elif choice == "5":
            display_datamem()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Try again.")
        if "0x"+CORE.pc not in machinecode and int("0x"+CORE.pc,16)<int(max(machinecode.keys()),16):
                print("Invalid PC")
                break
main() 