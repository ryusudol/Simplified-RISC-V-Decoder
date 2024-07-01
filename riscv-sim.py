import sys


def return_opcode(opcode):
    if opcode == '0110011': return 'r'          # Arithmetic / Logical Operations
    elif opcode == '0010011': return 'i'        # Immediate Operations
    elif opcode == '0000011': return 'load'     # Load Operations
    elif opcode == '0100011': return 's'        # Store Operations
    elif opcode == '0110111': return 'u'        # lui operation
    elif opcode == '1100011': return 'sb'       # Branch Operations
    elif opcode == '1100111': return 'return'
    elif opcode == '1101111': return 'uj'       # jal oepration
    elif opcode == '0010111': return 'auipc'
    else: return None

def return_r_operation(funct3, funct7):
    if funct3 == '000' and funct7 == '0000000': return 'add'
    elif funct3 == '000' and funct7 == '0100000': return 'sub'
    elif funct3 == '001' and funct7 == '0000000': return 'sll'
    elif funct3 == '010' and funct7 == '0000000': return 'slt'
    elif funct3 == '011' and funct7 == '0000000': return 'sltu'
    elif funct3 == '100' and funct7 == '0000000': return 'xor'
    elif funct3 == '101' and funct7 == '0000000': return 'srl'
    elif funct3 == '101' and funct7 == '0100000': return 'sra'
    elif funct3 == '110' and funct7 == '0000000': return 'or'
    elif funct3 == '111' and funct7 == '0000000': return 'and'
    else: return None

def return_i_operation(funct3, funct7=None):
    if funct3 == '000': return 'addi'
    elif funct3 == '001' and funct7 == '0000000': return 'slli'
    elif funct3 == '010': return 'slti'
    elif funct3 == '011': return 'sltiu'
    elif funct3 == '100': return 'xori'
    elif funct3 == '101' and funct7 == '0000000': return 'srli'
    elif funct3 == '101' and funct7 == '0100000': return 'srai'
    elif funct3 == '110': return 'ori'
    elif funct3 == '111': return 'andi'
    return None

def return_load_operation(funct3):
    if funct3 == '000': return 'lb'
    elif funct3 == '001': return 'lh'
    elif funct3 == '010': return 'lw'
    elif funct3 == '100': return 'lbu'
    elif funct3 == '101': return 'lhu'
    else: return None

def return_s_operation(funct3):
    if funct3 == '000': return 'sb'
    elif funct3 == '001': return 'sh'
    elif funct3 == '010': return 'sw'
    else: return None

def return_sb_operation(funct3):
    if funct3 == '000': return 'beq'
    elif funct3 == '001': return 'bne'
    elif funct3 == '100': return 'blt'
    elif funct3 == '101': return 'bge'
    elif funct3 == '110': return 'bltu'
    elif funct3 == '111': return 'bgeu'
    else: return None

def return_return_operation(funct3):
  if funct3 == '000': return 'jalr'
  else: return None

def return_immediate(imm_binary, format_type):
    binary = int(imm_binary[1:], 2)
    if imm_binary[0] == '0':
        if format_type == "sb" or format_type == "jal": return binary << 1
        elif format_type == "auipc" or format_type == "lui": return binary << 12
        else: return binary
    else:
        if format_type == "sb": return ((-1 << 12) + (binary << 1))
        elif format_type == "jal": return ((-1 << 20) + (binary << 1))
        elif format_type == "auipc" or format_type == "lui": return ((-1 << 31) + (binary << 12))
        else: return ((-1 << 11) + binary)

def print_instruction(instruction_number, instruction): 
    opcode = instruction[25:]
    format_type = return_opcode(opcode)
    rd = int(instruction[20:25], 2)
    funct3 = instruction[17:20]
    rs1 = int(instruction[12:17], 2)
    rs2 = int(instruction[7:12], 2)
    funct7 = instruction[0:7]
    inst_hex = hex(int(instruction, 2))[2:].zfill(8)
  
    if format_type == 'r':
        operation = return_r_operation(funct3, funct7)
        if operation: print(f"inst {instruction_number}: {inst_hex} {operation} x{rd}, x{rs1}, x{rs2}")
        else: print(f"inst {instruction_number}: {inst_hex} unknown instruction")
    
    elif format_type == 'i':
        operation = return_i_operation(funct3)
        if operation:
            immediate = return_immediate(instruction[:12], format_type)
            print(f"inst {instruction_number}: {inst_hex} {operation} x{rd}, x{rs1}, {immediate}")
        else:
            operation = return_i_operation(funct3, funct7)
            shamt = int(instruction[7:12], 2)
            if operation: print(f"inst {instruction_number}: {inst_hex} {operation} x{rd}, x{rs1}, {shamt}")
            else: print(f"inst {instruction_number}: {inst_hex} unknown instruction")

    elif format_type == 'load':
        operation = return_load_operation(funct3)
        immediate = return_immediate(instruction[:12], format_type)
        if operation: print(f"inst {instruction_number}: {inst_hex} {operation} x{rd}, {immediate}(x{rs1})")
        else: print(f"inst {instruction_number}: {inst_hex} unknown instruction")

    elif format_type == 's':
        operation = return_s_operation(funct3)
        imm_binary = instruction[:7] + instruction[20:25]
        immediate = return_immediate(imm_binary, format_type)
        if operation: print(f"inst {instruction_number}: {inst_hex} {operation} x{rs2}, {immediate}(x{rs1})")
        else: print(f"inst {instruction_number}: {inst_hex} unknown instruction")
        
    elif format_type == 'u':
        operation = 'lui'
        immediate = return_immediate(instruction[0:20], operation)
        if operation: print(f"inst {instruction_number}: {inst_hex} {operation} x{rd}, {immediate}")
        else: print(f"inst {instruction_number}: {inst_hex} unknown instruction")

    elif format_type == 'sb':
        operation = return_sb_operation(funct3)
        imm_binary = instruction[0] + instruction[24] + instruction[1:7] + instruction[20:24]
        immediate =  return_immediate(imm_binary, format_type)
        if operation: print(f"inst {instruction_number}: {inst_hex} {operation} x{rs1}, x{rs2}, {immediate}")
        else: print(f"inst {instruction_number}: {inst_hex} unknown instruction")

    elif format_type == 'return':
        operation = return_return_operation(funct3) 
        immediate = return_immediate(instruction[:12], format_type)
        if operation: print(f"inst {instruction_number}: {inst_hex} {operation} x{rd}, {immediate}(x{rs1})")
        else: print(f"inst {instruction_number}: {inst_hex} unknown instruction")
  
    elif format_type == 'uj':
        operation = 'jal'
        imm_binary = instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11]
        immediate = return_immediate(imm_binary, operation)
        if operation: print(f"inst {instruction_number}: {inst_hex} {operation} x{rd}, {immediate}")
        else: print(f"inst {instruction_number}: {inst_hex} unknown instruction")

    elif format_type == 'auipc':
        operation = format_type
        immediate = return_immediate(instruction[0:20], format_type)
        if operation: print(f"inst {instruction_number}: {inst_hex} {operation} x{rd}, {immediate}")
        else: print(f"inst {instruction_number}: {inst_hex} unknown instruction")

    else :
        print(f"inst {instruction_number}: {inst_hex} unknown instruction")


f_path = sys.argv[1]
with open(f_path, 'rb') as binary_input:
    instructions = binary_input.read()
    for idx in range(len(instructions) // 4):
        instruction = [ instructions[idx * 4 + 3], instructions[idx * 4 + 2], instructions[idx * 4 + 1], instructions[idx * 4] ]
        binary_instruction = ''
        for byte in instruction:
            binary_instruction += f"{byte:08b}"
        print_instruction(idx, binary_instruction)
