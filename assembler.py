import re
import sys

Instructions = {
    "add": {"opcode": "00000"},
    "sub": {"opcode": "00001"},
    "mov": {"opcode": ["00011","00010"]},
    "ld":  {"opcode": "00100"},
    "st":  {"opcode": "00101"},
    "mul": {"opcode": "00110"},
    "div": {"opcode": "00111"},
    "rs":  {"opcode":"01000"},
    "ls":  {"opcode":"01001"},
   "xor":  {"opcode":"01010"},
   "rs":   {"opcode":"01000"},
   "or":   {"opcode":"01011"},
   "and":  { "opcode":"01100"},
   "not":  {"opcode":"01101"},
   "cmp":  {"opcode":"01110"},
   "jmp":  {"opcode": "01111"},
   "jlt":  {"opcode": "11100"},
   "jgt":  {"opcode": "11101"},
   "je":   {"opcode": "11111"},
   "hlt":  {"opcode": "11010"}
}

regs_binary = {"R0" : '000',"R1" : '001', "R2" : '010', "R3" : '011', "R4" : '100', "R5" : '101', "R6" : '110', "FLAGS" : '111'}

# define regex patterns for scanning patterns
#label_pattern = r'^\s*([a-zA-Z_][a-zA-Z0-9_]*):(\s*(.*))?$' 
label_pattern = r'^\s*([a-zA-Z_][a-zA-Z0-9_]*):(\s*(.*))$'
l_pattern = r'^\s*end:\s*hlt$'

instruction_pattern = r'^\s*(hlt|ld|st|mov|add|sub|mul|div|ls|rs|xor|and|not|jmp|jlt|jgt|je|cmp)\s+'
instruction_pattern += r'(R[0-6]|FLAGS|([a-zA-Z_][a-zA-Z0-9_]*))?\s*'
instruction_pattern += r'(R[0-6]|FLAGS|([a-zA-Z_][a-zA-Z0-9_]*))?\s*'
instruction_pattern += r'(R[0-6]|FLAGS|([a-zA-Z_][a-zA-Z0-9_]*))?\s*'
instruction_pattern += r'(\s+(\$[0-99]{1,7}|[a-zA-Z_][a-zA-Z0-9_]*))?\s*\n?$'

variable_pattern = r'^\s*var\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*$'

#patterns for error handling
err_inst_pattern = r"\b\s*(hlt|ld|st|mov|add|sub|mul|div|ls|rs|xor|and|not|jmp|jlt|jgt|je|cmp)\s*\b"

# initialize dictionary for storing labels, instructions, and variables
program_dict = {'labels': {}, 'instructions': {}, 'variables': {}}

#temp values
ll = 0 #label lines
lh = 0 #label halt
ih = 0 #instruction halt
num_gen = -1
lv = 0 #track record of post : instructions
lb = 0
space_tab = "" #track spaces and tabs for label inst
temp_lab = None
lab_det = 0
lab_inst_count = 0
z = 0 #count lines of label inst
t_lab = 0 #temp value for checking if any label before instructions
num_zero = 0
temp = None
program_counter = 0
temp_dict = {}
x = 0 #check for error
line_check = 0 #count number of lines
label_check = 0 #count number of lines of label
inst_check = 0 #count number of lines of instructions

#defining helper functions

def dec_to_bin(num):
    new_num = '{:07b}'.format(num) #padding immideate to 7 bits
    return new_num

def bin_to_dec(binary):
    return int(binary,2)

def check_label(operation):
    x = ""
    x_temp = []
    if ":" in operation:
        i=operation.index(":")
        parts=operation.split(":")
        s=parts[0]
        t = parts[0]
        for j in operation[i+1:]:
            if(j==' ' or j=='\t'):
                x+=j
            elif(j.isalpha()==True):
                break
        s = parts[1].strip()
        x_temp = [t,x,s]

    else:
        x_temp = [0,"",0]
    return x_temp


#open file and read contents
with open('/home/akanksh/Downloads/assembler.txt', 'r') as f:
    lines = f.readlines()

#lines = []
#for kx in sys.stdin:
#    lines.append(kx)
lines = sys.stdin.readlines()
#print(lines)

# loop through lines in file and identify labels, instructions, and variables
lines[-1]=lines[-1]+'\n'+'\n'
#print(lines)
for line in lines:
    #print(line)
    line_check += 1
    label_match = re.match(label_pattern, line)
    label_new_match = re.match(l_pattern,line)
    temp = check_label(line)

    #Error Handling
    err_inst_match = re.match(err_inst_pattern,line)
    instruction_match = re.match(instruction_pattern, line)
    variable_match = re.match(variable_pattern, line)

    if variable_match:
        if label_check != 0 or inst_check != 0:
            print(f"Variables not declared at the beginning at line {line_check}")
            x = 1
            break

    elif err_inst_match:
        if instruction_match == None:
            print(f"Typos in instruction name or register name in line {line_check}")
            x = 1
            break
        
    elif temp[1] == "":
        if instruction_match == None:
            if variable_match == None:
                #print(line)
                print(f"General Syntax Error in line {line_check}")
                x = 1
                break

    val_reg = 0 #assumed initially Register has no value
    imm_check = -1 #if no immideate value return -1

    if temp[1] != "":
        label_check += 1
        label = temp[0] 
        space_tab = temp[1]  
        inst_label = temp[2]

        temp_dict[label] = dec_to_bin(program_counter)
        #print(space_tab)
        #print(inst_label)
        lab_det = 1

        #print(inst_label)
        if inst_label == 'hlt':
            program_dict['labels'][label] = {'value': 1}
        else:
            ll = 1
        lab_inst = [inst_label]
        program_dict['labels'][label] = {'label_instructions': lab_inst,'spaces_or_tabs' : space_tab, 'line' : line_check}

        if t_lab == 1:
            program_dict['labels'][label] = {'in_val' : 1}
        
        instruction_match = re.match(instruction_pattern, inst_label)
        if instruction_match:
            program_counter += 1
            instruction = instruction_match.group(1)
            operands = []
            imm = None
            imm_check = -1
            new_imm = -1
            inst = instruction_match.group(1)
            #print(inst)
            if inst == 'hlt':
                if ll != 0:
                    program_dict['labels'][label] = {'value': 1}
                    ll = 0
                else:
                    ih += 1

            for i in range(2, instruction_match.lastindex+1):
                operand = instruction_match.group(i)
                if operand:
                    if '$' in operand[1:].strip():
                        imm = int(operand[2:])
                        if imm > 127:
                            print(f"Illegal Immediate values (more than 7 bits) in line {line_check}")
                            x = 1
                            break        
                        #bin_imm = (bin(imm)[2:]) #converting num to binary
                        new_imm = dec_to_bin(imm) #padding immideate to 7 bits
                        #applying mov
                        val_reg = '{:016b}'.format(imm) #padding register value to 16 bits
                        #print(val_reg)
                        #print(imm)
                        imm_check = new_imm
                    else:
                        operands.append(operand.strip())
                        #i+=1

        if inst_label == 'hlt':
            program_dict['instructions'][inst_label] = {'opcode': 'hlt', 'operands': 0, 'imm': -1,'line' : line_check}
            lv+=1

        elif inst_label in program_dict['instructions']:
            program_dict['instructions'][num_gen] = {'opcode': instruction, 'operands': operands, 'imm': new_imm,'line' : line_check}
            num_gen+=1
            lv+=1
        else:
            program_dict['instructions'][inst_label] = {'opcode': instruction, 'operands': operands, 'imm': new_imm,'line' : line_check}
            lv+=1

        if len(program_dict['instructions'].keys()) - lv == 0:
            #print("hi")
            #print(program_dict['labels'][label])
            num_gen+=1
            program_dict['labels'][label]['new_val'] =num_gen
            #program_counter += 1 #counting label as line

        else:
            program_dict['labels'][label]['new_val'] = -1

    else:
        # check for instruction
        instruction_match = re.match(instruction_pattern, line)
        if instruction_match:
            inst_check += 1
            program_counter += 1

            if line.strip() != line[:-1]: #checking for label instructions with improper spacing
                lb+=1

            instruction = instruction_match.group(1)

            #checking halt for last instruction
            if instruction == "hlt":
                if line_check != len(lines):
                    print("hlt not being used as the last instruction")

            #print(instruction)
            operands = []
            imm = None
            imm_check = -1
            new_imm = -1

            if temp_lab != None and lab_det != 0:
                #print(temp_lab)
                #print(program_dict)
                i = program_dict['labels'][temp_lab]['spaces_or_tabs']
                t_l = i + line.strip()
                t_line = line[:-1]
                #print(t_line)
                if t_l == t_line:
                    #print("yes")
                    lab_inst.append(line.strip())
                    program_dict['labels'][temp_lab] = {'label_instructions' : lab_inst}
                    lab_inst_count += 1
                    #print(program_dict)

            inst = instruction_match.group(1)
            #print(inst)

            for i in range(2, instruction_match.lastindex+1):
                operand = instruction_match.group(i)
                #print(operand)
                if operand:
                    if '$' in operand[1:].strip():
                        imm = int(operand[2:])
                        if imm > 127:
                            print(f"Illegal Immediate values (more than 7 bits) in line {line_check}")
                            x = 1
                            break
            
                        new_imm = dec_to_bin(imm) #padding immideate to 7 bits
                        #applying mov
                        val_reg = '{:016b}'.format(imm) #padding register value to 16 bits
                        #print(val_reg)
                        #print(imm)
                        imm_check = new_imm
                    else:
                        operands.append(operand.strip())

            if label_match:
                program_dict['labels'][label]['label_instructions'] = {'opcode': instruction, 'operands': operands, 'imm': new_imm,'line' : line_check}
            else:
                if line.strip() in program_dict['instructions']:
                    program_dict['instructions'][num_gen] = {'opcode': instruction, 'operands': operands, 'imm': imm_check,'line' : line_check}    
                    num_gen+=1

                else:
                    program_dict['instructions'][line.strip()] = {'opcode': instruction, 'operands': operands, 'imm': imm_check,'line' : line_check}

            if program_dict['instructions'][line.strip()] == {'opcode': 'mov', 'operands': operands, 'imm': new_imm,'line' : line_check}: #check if mov has 1 register and 1 immideate only
                program_dict['instructions'][line.strip()] = {'opcode': 'mov', 'operands': operands, 'imm': new_imm, 'val_reg' : val_reg,'line' : line_check}

            elif program_dict['instructions'][line.strip()] == {'opcode': 'hlt', 'operands': 1, 'imm': -1,'line' : line_check}: #check if mov has 1 register and 1 immideate only 
                pass
        else:
            # check for variable
            variable_match = re.match(variable_pattern, line)
            if variable_match:
                variable = variable_match.group(1)
                program_dict['variables'][variable] = None

if 'hlt' in program_dict['labels']:
    temp_var_val = len(program_dict["instructions"]) + len(program_dict['labels'])-2

else:
    temp_var_val = len(program_dict["instructions"]) + len(program_dict['labels'])-1

#print(temp_var_val)
x_l = []
for i in (program_dict['variables'].keys()):
    x_l.append(i)
#print(x_l)
temp_var_val -= lv

for i in range(0,len(x_l)):
    temp_var_val+=1
    #print(temp_var_val)
    #temp_var_val_2 = (bin(temp_var_val)[2:])
    var_val = dec_to_bin(temp_var_val)
    program_dict['variables'][x_l[i]] = var_val
#print(num_gen)
#print(program_dict,"\n")
#print(temp_dict)

result=[]
y = num_gen
var = 0
lab_0_val = 0 #to count number of labels before instructions

#Error Handling

for i in program_dict['instructions'].values():
    if i['opcode'] == 'hlt':
        y = 0
        break
    y = 2
    
if y == 2:
    print("Missing hlt instruction")

for i in program_dict['instructions'].values():

    if x == 1:
        break
    
    if i['opcode'] == 'add': #for add instruction 
        if i['imm']!= -1 and len(i['operands'])==2: #immideate error handling done
            print(f"General Syntax Error in line {i['line']}")
            x = 1
            break

        elif "FLAGS" in i['operands']:
            print(f"Illegal use of FLAGS register in line {i['line']}")
            x = 2
            break 

        elif i['imm'] == -1 and len(i['operands'])==3:
            result.append(Instructions['add']['opcode']+'00'+regs_binary[i['operands'][0]]+regs_binary[i['operands'][1]]+regs_binary[i['operands'][2]]) 

        else:
            print(f"General Syntax Error in line {i['line']}")
            x = 1
            break

    if i['opcode'] == 'sub': #for sub inst.
        if i['imm']!= -1 and len(i['operands'])==2: #immideate error handling done
              print(f"General Syntax Error in line {i['line']}")
              x = 1
              break
        
        elif "FLAGS" in i['operands']:
            print(f"Illegal use of FLAGS register in line {i['line']}")
            x = 2
            break

        elif i['imm'] == -1 and len(i['operands'])==3:
            result.append(Instructions['sub']['opcode']+'00'+regs_binary[i['operands'][0]]+regs_binary[i['operands'][1]]+regs_binary[i['operands'][2]])
        else:
              print(f"General Syntax Error in line {i['line']}")
              x = 1
              break

    if i['opcode'] == 'mul': #for mul inst.
        if i['imm']!= -1 and len(i['operands'])==2: #immideate error handling done
              print(f"General Syntax Error in line {i['line']}")
              x = 1
              break
        
        elif "FLAGS" in i['operands']:
            print(f"Illegal use of FLAGS register in line {i['line']}")
            x = 2
            break

        elif i['imm'] == -1 and len(i['operands'])==3:
            result.append(Instructions['mul']['opcode']+'00'+regs_binary[i['operands'][0]]+regs_binary[i['operands'][1]]+regs_binary[i['operands'][2]])
        else:
              print(f"General Syntax Error in line {i['line']}") 
              x = 1
              break

    if i['opcode'] == 'mov': #for move inst.
        if i['imm']!= -1 and len(i['operands'])==2: #immideate error handling done
            print(f"General Syntax Error in line {i['line']}")
            x = 1
            break
        elif i['imm'] != -1 and len(i['operands'])==1:
            result.append(Instructions['mov']['opcode'][1]+'0'+regs_binary[i['operands'][0]]+i['imm'])
        elif i['imm'] == -1 and len(i['operands'])==2:
            result.append(Instructions['mov']['opcode'][0]+'0'*5+regs_binary[i['operands'][0]]+regs_binary[i['operands'][1]])
        else:
            print(f"General Syntax Error in line {i['line']}")
            x = 1
            break
    
    if i['opcode'] == 'ld': #for load inst.
        var = i['operands'][1]
        #print(var)
        if len(i['operands'])==2:
            if var in x_l:
                result.append(Instructions['ld']['opcode']+'0'+regs_binary[i['operands'][0]]+program_dict['variables'][var])

            elif i['operands'][1] in program_dict['labels'].keys():
                print(f"Misuse of labels as variables in line {i['line']}")
                x = 2
                break

            else:
                print(f"Use of undefined variables in line {i['line']}")
                x = 1
                break
        else:
                print(f"General Syntax Error in line {i['line']}")
                x = 1
                break

    if i['opcode'] == 'st': #for store inst.
        var = i['operands'][1]
        #print(var)
        if len(i['operands'])==2:
            if var in x_l:
                result.append(Instructions['st']['opcode']+'0'+regs_binary[i['operands'][0]]+program_dict['variables'][var])

            elif i['operands'][1] in program_dict['labels'].keys():
                print(f"Misuse of labels as variables in line {i['line']}")
                x = 2
                break

            else:
                print(f"Use of undefined variables in line {i['line']}")
                x = 1
                break
        else:
                print(f"General Syntax Error in line {i['line']}")
                x =1
                break

    if i['opcode'] == 'div': #for divide inst.
        if i['imm']!= -1 and len(i['operands'])!=2: #immideate error handling done
            print(f"General Syntax Error in line {i['line']}")
            x = 1
            break

        elif "FLAGS" in i['operands']:
            print(f"Illegal use of FLAGS register in line {i['line']}")
            x = 2
            break

        elif i['imm'] == -1 and len(i['operands'])==2:
           result.append(Instructions['div']['opcode']+'0'*5+regs_binary[i['operands'][0]]+regs_binary[i['operands'][1]])
        else:
            print(f"General Syntax Error in line {i['line']}")
            x = 1
            break
      
    if i['opcode'] == 'ls': #for left shift inst.
        if i['imm'] == -1 and len(i['operands']) == 2: #immideate error handling done
            print("General Syntax Error")
            x = 1
            break

        elif "FLAGS" in i['operands']:
            print(f"Illegal use of FLAGS register in line {i['line']}")
            x = 2
            break

        elif i['imm'] != -1 and len(i['operands'])==1:
            result.append(Instructions['ls']['opcode']+'0'+regs_binary[i['operands'][0]]+i['imm'])
        else:
            print(f"General Syntax Error in line {i['line']}")
            x = 1
            break

    if i['opcode'] == 'rs': #for right shift inst.
        if i['imm'] == -1 and len(i['operands']) == 2: #immideate error handling done
            print(f"General Syntax Error in line {i['line']}")
            x = 1
            break

        elif "FLAGS" in i['operands']:
            print(f"Illegal use of FLAGS register in line {i['line']}")
            x = 2
            break

        elif i['imm'] != -1 and len(i['operands'])==1:
            result.append(Instructions['rs']['opcode']+'0'+regs_binary[i['operands'][0]]+i['imm'])
        else:
            print(f"General Syntax Error in line {i['line']}")
            x = 1
            break

    if i['opcode'] == 'xor': #for xor inst.
        if i['imm']!= -1: #immideate error handling done
              print(f"General Syntax Error in line {i['line']}")
              x = 1
              break
        
        elif "FLAGS" in i['operands']:
            print(f"Illegal use of FLAGS register in line {i['line']}")
            x = 2
            break

        elif i['imm'] == -1 and len(i['operands'])==3:
            result.append(Instructions['xor']['opcode']+'00'+regs_binary[i['operands'][0]]+regs_binary[i['operands'][1]]+regs_binary[i['operands'][2]])
        else:
              print(f"General Syntax Error in line {i['line']}")
              x = 1
              break

    if i['opcode'] == 'or': #for or inst.
        if i['imm']!= -1: #immideate error handling done
              print(f"General Syntax Error in line {i['line']}")
              x = 1
              break
        
        elif "FLAGS" in i['operands']:
            print(f"Illegal use of FLAGS register in line {i['line']}")
            x = 2
            break

        elif i['imm'] == -1 and len(i['operands'])==3:
            result.append(Instructions['or']['opcode']+'00'+regs_binary[i['operands'][0]]+regs_binary[i['operands'][1]]+regs_binary[i['operands'][2]])
        else:
              print(f"General Syntax Error in line {i['line']}") 
              x=1  
              break

    if i['opcode'] == 'and': #for and inst.
        if i['imm']!= -1: #immideate error handling done
             print(f"General Syntax Error in line {i['line']}")
             x=1
             break
       
        elif "FLAGS" in i['operands']:
            print(f"Illegal use of FLAGS register in line {i['line']}")
            x = 2
            break
       
        elif i['imm'] == -1 and len(i['operands'])==3:
           result.append(Instructions['and']['opcode']+'00'+regs_binary[i['operands'][0]]+regs_binary[i['operands'][1]]+regs_binary[i['operands'][2]])
        else:
             print(f"General Syntax Error in line {i['line']}")
             x=1 
             break

    if i['opcode'] == 'not': #for Invert inst.
        if i['imm']!= -1 and len(i['operands'])!=2: #immideate error handling done
            print(f"General Syntax Error in line {i['line']}")
            x=1
            break

        elif "FLAGS" in i['operands']:
            print(f"Illegal use of FLAGS register in line {i['line']}")
            x = 2
            break

        elif i['imm'] == -1 and len(i['operands'])==2:
            result.append(Instructions['not']['opcode']+'0'*5+regs_binary[i['operands'][0]]+regs_binary[i['operands'][1]])
        else:
            print(f"General Syntax Error in line {i['line']}")
            x=1 
            break

    if i['opcode'] == 'cmp': #for Compare inst.
        if i['imm']!= -1 and len(i['operands'])!=2: #immideate error handling done
            print(f"General Syntax Error in line {i['line']}")
            x=1
            break

        elif "FLAGS" in i['operands']:
            print(f"Illegal use of FLAGS register in line {i['line']}")
            x = 2
            break

        elif i['imm'] == -1 and len(i['operands'])==2:
            result.append(Instructions['cmp']['opcode']+'0'*5+regs_binary[i['operands'][0]]+regs_binary[i['operands'][1]])
        else:
            print(f"General Syntax Error in line {i['line']}")
            x=1    
            break

    if i['opcode'] == 'jmp': #for jump inst.
        if len(i['operands'])==1:
            #print(program_dict['labels'])
            for j in program_dict['labels']:
                #print(j,i['operands'][0])
                if (i['operands'][0]).strip() == j:
                    #print(Instructions['jmp']['opcode']+'0'*4+temp_dict[i['operands'][0]])
                    result.append(Instructions['jmp']['opcode']+'0'*4+temp_dict[i['operands'][0]])
                    x = 0
                    break

                elif (i['operands'][0]).strip() in program_dict['variables'].keys():
                    print(f"Misuse of variables as labels in line {i['line']}")
                    x = 2

                else:
                    x=1
                    
            if x ==1:
                print(f"Use of undefined labels in line {i['line']}")
                break
                    
        else:
                print(f"General Syntax Error in line {i['line']}")
                x=1
                break

    if i['opcode'] == 'jlt': #for jump if less than inst.
        if len(i['operands'])==1:
            for j in program_dict['labels']:
                if (i['operands'][0]).strip() == j:
                    #print(Instructions['jgt']['opcode']+'0'*4+temp_dict[i['operands'][0]])
                    result.append(Instructions['jlt']['opcode']+'0'*4+temp_dict[i['operands'][0]])
                    x = 0
                    break

                elif (i['operands'][0]).strip() in program_dict['variables'].keys():
                    print(f"Misuse of variables as labels in line {i['line']}")
                    x = 2        

                else:
                    x=1
                    
            if x ==1:
                print(f"Use of undefined labels in line {i['line']}")
                break

        else:
             print(f"General Syntax Error in line {i['line']}")
             x=1
             break

    if i['opcode'] == 'jgt': #for jump inst.
        #t_label = temp_dict[i['operands'][0]]
        if len(i['operands'])==1:
            for j in program_dict['labels']:
                if (i['operands'][0]).strip() == j:
                    #print(Instructions['jgt']['opcode']+'0'*4+temp_dict[i['operands'][0]])
                    result.append(Instructions['jgt']['opcode']+'0'*4+temp_dict[i['operands'][0]])
                    x = 0
                    break
                elif (i['operands'][0]).strip() in program_dict['variables'].keys():
                    print(f"Misuse of variables as labels in line {i['line']}")
                    x = 2
                    break

                else:
                    x=1
                    
            if x ==1:
                print(f"Use of undefined labels in line {i['line']}")
                break

        else:
             print(f"General Syntax Error in line {i['line']}")
             x=1
             break

    if i['opcode'] == 'je': #for jump inst.
        if len(i['operands'])==1:
            for j in program_dict['labels']:
                if (i['operands'][0]).strip() == j:
                    #print(Instructions['jgt']['opcode']+'0'*4+temp_dict[i['operands'][0]])
                    result.append(Instructions['je']['opcode']+'0'*4+temp_dict[i['operands'][0]])
                    x = 0
                    break

                elif (i['operands'][0]).strip() in program_dict['variables'].keys():
                    print(f"Misuse of variables as labels in line {i['line']}")
                    x = 2
                    
                else:
                    x=1
  
            if x ==1:
                print(f"Use of undefined labels in line {i['line']}")
                break

        else:
             print(f"General Syntax Error in line {i['line']}")
             x=1
             break

    if i['opcode'] == 'hlt': #for halt inst.
        result.append(Instructions['hlt']['opcode']+'0'*11)

if x == 0 and y == 0:
    if len(result)<127:
    	length = len(result)
    else:
        length = 127
    for i in range(length): # The assembler can write less than or equal to 128 lines.
        l = result[i].strip()
        if i!=len(result)-1:
            sys.stdout.write(l+'\n')
        else:
            sys.stdout.write(l)
