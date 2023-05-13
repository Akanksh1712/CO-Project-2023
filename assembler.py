import re

Instructions = {
    "add": {"opcode": "00000", "operands": 3, "addressing_modes": ["reg", "mem"]},
    "sub": {"opcode": "00001", "operands": 3, "addressing_modes": ["reg", "mem"]},
    "mov": {"opcode": "00010", "operands": 2, "addressing_modes": ["imm", "reg", "mem"]},
    "ld": {"opcode": "00100", "operands": 1, "addresing_modes": ["reg", "mem"]},
    "st": {"opcode": "00101", "operands": 1, "addressing_modes": ["reg", "mem"]},
    "mul": {"opcode": "00110", "operands": 2, "addressing_modes": ["reg", "mem"]},
    "div": {"opcode": "00111", "operands": 2, "addressing_modes": ["reg", "mem"]},
    "rs": {"opcode":"01000", "operands": 1, "addressing_modes": ["reg", "imm"]},
    "ls":{"opcode":"01001", "operands": 1, "addressing_modes": ["reg", "imm"]},
   "xor":{ "opcode":"01010", "operands": 3, "addressing_modes": ["reg", "mem"]},
   "rs":{ "opcode":"01000", "operands": 2, "addressing_modes": ["reg", "mem"]},
   "ls":{ "opcode":"01001", "operands": 2, "addressing_modes": ["reg", "mem"]},
   "or":{ "opcode":"01011", "operands": 3, "addressing_modes": ["reg", "mem"]},
   "and":{ "opcode":"01100", "operands": 3, "addressing_modes": ["reg", "mem"]},
   "not":{ "opcode":"01101", "operands": 2, "addressing_modes": ["reg", "mem"]},
   "cmp":{ "opcode":"01110", "operands": 2, "addressing_modes": ["reg", "mem"]},
   "jmp": {"opcode": "01111", "operands": 1, "addressing_modes": ["mem"]},
   "jlt": {"opcode": "11100", "operands": 1, "addressing_modes": ["mem"]},
   "jgt": {"opcode": "11101", "operands": 1, "addressing_modes": ["mem"]},
   "je": {"opcode": "11111", "operands": 1, "addressing_modes": ["mem"]},
   "hlt": {"opcode": "11010", "operands": 1, "addressing_modes": []}
}

regs_binary = {"R0" : '000',"R1" : '001', "R2" : '010', "R3" : '011', "R4" : '100', "R5" : '101', "R6" : '110', "FLAGS" : '111'}

# define regex patterns for scanning patterns
label_pattern = r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:$'

instruction_pattern = r'^\s*(hlt|ld|st|mov|add|sub|mul|jmp|jz|jnz|cmp)\s+'
instruction_pattern += r'(R[0-6]|FLAGS|([a-zA-Z_][a-zA-Z0-9_]*))?\s*'
instruction_pattern += r'(R[0-6]|FLAGS|([a-zA-Z_][a-zA-Z0-9_]*))?\s*'
instruction_pattern += r'(R[0-6]|FLAGS|([a-zA-Z_][a-zA-Z0-9_]*))?\s*'
instruction_pattern += r'(\s+(\#[0-99]{1,7}|[a-zA-Z_][a-zA-Z0-9_]*))?\s*$'

variable_pattern = r'^\s*var\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*$'

# initialize dictionary for storing labels, instructions, and variables
program_dict = {'labels': {}, 'instructions': {}, 'variables': {}}

# open file and read contents
with open('CO-Project-2023/assembler.txt', 'r') as f:
    lines = f.readlines()

# loop through lines in file and identify labels, instructions, and variables
for line in lines:
    val_reg = 0 #assumed initially Register has no value
    imm_check = -1 #if no immideate value return -1

    # check for label
    label_match = re.match(label_pattern, line)
    if label_match:
        label = label_match.group(1)
        program_dict['labels'][label] = {'label_instructions': []}

    # check for instruction
    instruction_match = re.match(instruction_pattern, line)
    if instruction_match:
        instruction = instruction_match.group(1)
        operands = []
        imm = None
        for i in range(2, instruction_match.lastindex+1):
            operand = instruction_match.group(i)
            if operand:
                if '#' in operand[1:].strip():
                    imm = int(operand[2:])
                    bin_imm = (bin(imm)[2:]) #converting num to binary
                    new_imm = '{:07b}'.format(imm) #padding immideate to 7 bits
                    #applying mov
                    val_reg = '{:016b}'.format(imm) #padding register value to 7 bits
                    #print(val_reg)
                    #print(imm)
                    imm_check = new_imm
                else:
                    operands.append(operand.strip())
                    #i+=1
        
        if label_match:
            program_dict['labels'][label]['label_instructions'].append({'opcode': instruction, 'operands': operands, 'imm': new_imm})
        else:
            program_dict['instructions'][line.strip()] = {'opcode': instruction, 'operands': operands, 'imm': imm_check}

        if program_dict['instructions'][line.strip()] == {'opcode': 'mov', 'operands': operands, 'imm': new_imm}: #check if mov has 1 register and 1 immideate only
            program_dict['instructions'][line.strip()] = {'opcode': 'mov', 'operands': operands, 'imm': new_imm, 'val_reg' : val_reg}

    else:
        # check for variable
        variable_match = re.match(variable_pattern, line)
        if variable_match:
            variable = variable_match.group(1)
            program_dict['variables'][variable] = None
  

print(program_dict)

for i in program_dict['instructions'].values():
    if i['opcode'] == 'add': #for add instruction 
      if i['imm']!= -1 and len(i['operands'])==2: #immideate error handling done
          print("Immideate given for add instruction with 2 registers")
      elif i['imm'] == -1 and len(i['operands'])==3:
          print(Instructions['add']['opcode']+'00'+regs_binary[i['operands'][0]]+regs_binary[i['operands'][1]]+regs_binary[i['operands'][2]])
      else:
          print("Invalid format for add instruction")

    if i['opcode'] == 'sub': #for sub inst.
        if i['imm']!= -1 and len(i['operands'])==2: #immideate error handling done
              print("Immideate given for sub instruction with 2 registers")
        elif i['imm'] == -1 and len(i['operands'])==3:
            print(Instructions['sub']['opcode']+'00'+regs_binary[i['operands'][0]]+regs_binary[i['operands'][1]]+regs_binary[i['operands'][2]])
        else:
              print("Invalid format for sub instruction")

    if i['opcode'] == 'mul': #for mul inst.
        if i['imm']!= -1 and len(i['operands'])==2: #immideate error handling done
              print("Immideate given for mul instruction with 2 registers")
        elif i['imm'] == -1 and len(i['operands'])==3:
            print(Instructions['mul']['opcode']+'00'+regs_binary[i['operands'][0]]+regs_binary[i['operands'][1]]+regs_binary[i['operands'][2]])
        else:
              print("Invalid format for mul instruction") 

    if i['opcode'] == 'mov': #for move inst.
        if i['imm']!= -1 and len(i['operands'])==2: #immideate error handling done
              print("Immideate given for sub instruction with 2 registers")
        elif i['imm'] != -1 and len(i['operands'])==1:
            print(Instructions['mov']['opcode']+'0'+regs_binary[i['operands'][0]]+i['imm'])
        elif i['imm'] == -1 and len(i['operands'])==2:
            print(Instructions['mov']['opcode']+'0'*5+regs_binary[i['operands'][0]]+regs_binary[i['operands'][1]])
        else:
              print("Invalid format for mov instruction")

