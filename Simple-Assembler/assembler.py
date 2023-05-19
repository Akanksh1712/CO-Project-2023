import re
import sys

Instructions = {
    "add": {"opcode": "00000", "operands": 3, "addressing_modes": ["reg", "mem"]},
    "sub": {"opcode": "00001", "operands": 3, "addressing_modes": ["reg", "mem"]},
    "mov": {"opcode": ["00011","00010"], "operands": 2, "addressing_modes": ["imm", "reg", "mem"]},
    #"movi": {"opcode": "00010", "operands": 2, "addressing_modes": ["imm", "reg", "mem"]},
    "ld": {"opcode": "00100", "operands": 1, "addresing_modes": ["reg", "mem"]},
    "st": {"opcode": "00101", "operands": 1, "addressing_modes": ["reg", "mem"]},
    "mul": {"opcode": "00110", "operands": 2, "addressing_modes": ["reg", "mem"]},
    "div": {"opcode": "00111", "operands": 2, "addressing_modes": ["reg", "mem"]},
    "rs": {"opcode":"01000", "operands": 1, "addressing_modes": ["reg", "imm"]},
    "ls":{"opcode":"01001", "operands": 1, "addressing_modes": ["reg", "imm"]},
   "xor":{ "opcode":"01010", "operands": 3, "addressing_modes": ["reg", "mem"]},
   "rs":{ "opcode":"01000", "operands": 2, "addressing_modes": ["reg", "mem"]},
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
#label_pattern = r'^\s*([a-zA-Z_][a-zA-Z0-9_]*):(\s*(.*))?$'
label_pattern = r'^\s*([a-zA-Z_][a-zA-Z0-9_]*):(\s*(.*))$'
l_pattern = r'^\s*end:\s*hlt$'


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

#print(check_label("lab:	add R3 R2 R1"))

instruction_pattern = r'^\s*(hlt|ld|st|mov|add|sub|mul|div|ls|rs|xor|and|not|jmp|jlt|jgt|je|cmp)\s+'
instruction_pattern += r'(R[0-6]|FLAGS|([a-zA-Z_][a-zA-Z0-9_]*))?\s*'
instruction_pattern += r'(R[0-6]|FLAGS|([a-zA-Z_][a-zA-Z0-9_]*))?\s*'
instruction_pattern += r'(R[0-6]|FLAGS|([a-zA-Z_][a-zA-Z0-9_]*))?\s*'
instruction_pattern += r'(\s+(\$[0-99]{1,7}|[a-zA-Z_][a-zA-Z0-9_]*))?\s*\n?$'
#instruction_pattern = instruction_pattern.replace(' ', r'\s')

variable_pattern = r'^\s*var\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*$'

# initialize dictionary for storing labels, instructions, and variables
program_dict = {'labels': {}, 'instructions': {}, 'variables': {}}

#temp values
ll = 0 #label lines
lh = 0 #label halt
ih = 0 #instruction halt
num_gen = -1
lv = 0 #track record of post : instructions
space_tab = "" #track spaces and tabs for label inst
temp_lab = None
lab_det = 0
lab_inst_count = 0
z = 0 #count lines of label inst
t_lab = 0 #temp value for checking if any label before instructions
num_zero = 0


#open file and read contents
#with open('/home/akanksh/Downloads/assembler.txt', 'r') as f:
#    lines = f.readlines()

#lines = []
#for kx in sys.stdin:
#    lines.append(kx)
lines = sys.stdin.readlines()
#print(lines)
#with open('/home/akanksh/Downloads/assembler.txt', 'a') as z:
#    z.write('\n')
#    z.close()

#from sys import stdin
#from sys import stdout
##lines = stdin
#lines = sys.stdin.readlines()
#print(lines)

# loop through lines in file and identify labels, instructions, and variables
lines[-1]=lines[-1]+'\n'+'\n'
#print(lines)
for line in lines:
    #print(line)
    val_reg = 0 #assumed initially Register has no value
    imm_check = -1 #if no immideate value return -1

    temp = check_label(line)
    #print(temp)
    # check for label
    label_match = re.match(label_pattern, line)
    label_new_match = re.match(l_pattern,line)
    #print(label_new_match)

    if temp[1] != "":
        label = temp[0] 
        space_tab = temp[1]  
        inst_label = temp[2]

        #print(label)
        #print(space_tab)
        #print(inst_label)
        #print(program_dict['labels'][label])

        #if len(program_dict['instructions'].keys()) - lv == 0:
        #    print("hi")
        #    program_dict['labels'][label] = {'new_val' : num_gen}
        #    num_gen+=1
        lab_det = 1


        #label = label_match.group(1)
        #print(label)
#
        #temp_lab = label
        ##print(temp_lab)
        #inst_label = label_match.group(3).strip()
#
        #line_temp = line.split(':')
        #space_tab = ((len(label)+1)*" ") + ((line_temp[1].count('\t'))*'\t')
        #print(len(space_count))

        #print(inst_label)
        if inst_label == 'hlt':
            program_dict['labels'][label] = {'value': 1}
        else:
            ll = 1
        lab_inst = [inst_label]
        program_dict['labels'][label] = {'label_instructions': lab_inst,'spaces_or_tabs' : space_tab}

        if t_lab == 1:
            program_dict['labels'][label] = {'in_val' : 1}
        
        instruction_match = re.match(instruction_pattern, inst_label)
        if instruction_match:
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

            #if new_imm == 0:
            #    program_dict['labels'][label]['label_instructions'] = {'opcode': instruction, 'operands': operands, 'imm': new_imm}
            #else:
            #    program_dict['instructions'][line.strip()] = {'opcode': instruction, 'operands': operands, 'imm': imm_check}

            #if program_dict['instructions'][line.strip()] == {'opcode': 'mov', 'operands': operands, 'imm': new_imm}: #check if mov has 1 register and 1 immideate only
            #    program_dict['instructions'][line.strip()] = {'opcode': 'mov', 'operands': operands, 'imm': new_imm, 'val_reg' : val_reg}
#
            #elif program_dict['instructions'][line.strip()] == {'opcode': 'hlt', 'operands': 1, 'imm': -1}: #check if mov has 1 register and 1 immideate only 
            #    pass

        #if line.strip() in program_dict['labels']:
        #        program_dict['labels'][num_gen] = {'opcode': instruction, 'operands': operands, 'imm': new_imm}    
        #        num_gen+=1
        #else:
        #    program_dict['labels'][line.strip()] = {'opcode': instruction, 'operands': operands, 'imm': new_imm}

        #program_dict['instructions'][inst_label] = {'opcode': instruction, 'operands': operands, 'imm': new_imm}

        if inst_label == 'hlt':
            program_dict['instructions'][inst_label] = {'opcode': 'hlt', 'operands': 0, 'imm': -1}
            lv+=1

        elif inst_label in program_dict['instructions']:
            program_dict['instructions'][num_gen] = {'opcode': instruction, 'operands': operands, 'imm': new_imm}
            num_gen+=1
            lv+=1
        else:
            program_dict['instructions'][inst_label] = {'opcode': instruction, 'operands': operands, 'imm': new_imm}
            lv+=1

        if len(program_dict['instructions'].keys()) - lv == 0:
            #print("hi")
            #print(program_dict['labels'][label])
            num_gen+=1
            program_dict['labels'][label]['new_val'] =num_gen

        else:
            program_dict['labels'][label]['new_val'] = -1

        
    else:
        # check for instruction
        instruction_match = re.match(instruction_pattern, line)
        if instruction_match:
            instruction = instruction_match.group(1)
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
            #if inst == 'hlt':
            #    #print("yes")
            #    if ll != 0:
            #        #print("nno")
            #        program_dict['labels'][label] = {'value': 1}
            #        ll = 0
            #    else:
            #        ih 

            for i in range(2, instruction_match.lastindex+1):
                operand = instruction_match.group(i)
                #print(operand)
                if operand:
                    if '$' in operand[1:].strip():
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
                        #i+

            if label_match:
                program_dict['labels'][label]['label_instructions'] = {'opcode': instruction, 'operands': operands, 'imm': new_imm}
            else:
                if line.strip() in program_dict['instructions']:
                    program_dict['instructions'][num_gen] = {'opcode': instruction, 'operands': operands, 'imm': imm_check}    
                    num_gen+=1

                else:
                    program_dict['instructions'][line.strip()] = {'opcode': instruction, 'operands': operands, 'imm': imm_check}

            if program_dict['instructions'][line.strip()] == {'opcode': 'mov', 'operands': operands, 'imm': new_imm}: #check if mov has 1 register and 1 immideate only
                program_dict['instructions'][line.strip()] = {'opcode': 'mov', 'operands': operands, 'imm': new_imm, 'val_reg' : val_reg}

            elif program_dict['instructions'][line.strip()] == {'opcode': 'hlt', 'operands': 1, 'imm': -1}: #check if mov has 1 register and 1 immideate only 
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
    temp_var_val_2 = (bin(temp_var_val)[2:])
    var_val = '{:07b}'.format(temp_var_val)
    program_dict['variables'][x_l[i]] = var_val
#print(num_gen)
#print(program_dict)

result=[]
temp_dict = {}
x = 0
y = num_gen
var = 0
#print(program_dict['labels']['l1']['new_val'])

for i in program_dict['labels'].keys():
    
    #print(i['new_val'])
    #print(program_dict['labels'][i].keys())

    if i == 'hlt':
        program_dict['instructions'][i] = {'opcode' : 'hlt'}
        #del program_dict['labels'][i]

    #if program_dict['labels'][i] == 1:
    #    print("yes")

    elif program_dict['labels'][i]['new_val'] == 0:
        t_val = program_dict['labels'][i]['new_val']
        y = t_val
        t_val_2 = (bin(t_val)[2:])
        t_val = '{:07b}'.format(t_val)
        temp_dict[i] = t_val

    else:
        #print(lab_inst_count)
        #print(lv)
        #print(num_gen)
        #print(y)
        #print(len(program_dict['instructions']))
        temp_label_val = len(program_dict['instructions']) - (lab_inst_count+lv) + y
        temp_label_val_2 = (bin(temp_label_val)[2:])
        label_val = '{:07b}'.format(temp_label_val)
        temp_dict[i] = label_val
        y+=2
#print(temp_dict)

for i in program_dict['instructions'].values():
    if i['opcode'] == 'add': #for add instruction 
      if i['imm']!= -1 and len(i['operands'])==2: #immideate error handling done
          print("General Syntax Error")
          x = 1
          break
      elif i['imm'] == -1 and len(i['operands'])==3:
          result.append(Instructions['add']['opcode']+'00'+regs_binary[i['operands'][0]]+regs_binary[i['operands'][1]]+regs_binary[i['operands'][2]])
      else:
          print("General Syntax Error")
          x = 1
          break

    if i['opcode'] == 'sub': #for sub inst.
        if i['imm']!= -1 and len(i['operands'])==2: #immideate error handling done
              print("General Syntax Error")
              x = 1
              break
        elif i['imm'] == -1 and len(i['operands'])==3:
            result.append(Instructions['sub']['opcode']+'00'+regs_binary[i['operands'][0]]+regs_binary[i['operands'][1]]+regs_binary[i['operands'][2]])
        else:
              print("General Syntax Error")
              x = 1
              break

    if i['opcode'] == 'mul': #for mul inst.
        if i['imm']!= -1 and len(i['operands'])==2: #immideate error handling done
              print("General Syntax Error")
              x = 1
              break
        elif i['imm'] == -1 and len(i['operands'])==3:
            result.append(Instructions['mul']['opcode']+'00'+regs_binary[i['operands'][0]]+regs_binary[i['operands'][1]]+regs_binary[i['operands'][2]])
        else:
              print("General Syntax Error") 
              x = 1
              break

    if i['opcode'] == 'mov': #for move inst.
        if i['imm']!= -1 and len(i['operands'])==2: #immideate error handling done
            print("General Syntax Error")
            x = 1
            break
        elif i['imm'] != -1 and len(i['operands'])==1:
            result.append(Instructions['mov']['opcode'][1]+'0'+regs_binary[i['operands'][0]]+i['imm'])
        elif i['imm'] == -1 and len(i['operands'])==2:
            result.append(Instructions['mov']['opcode'][0]+'0'*5+regs_binary[i['operands'][0]]+regs_binary[i['operands'][1]])
        else:
            print("General Syntax Error")
            x = 1
            break
    
    if i['opcode'] == 'ld': #for load inst.
        var = i['operands'][1]
        #print(var)
        if len(i['operands'])==2:
            if var in x_l:
                result.append(Instructions['ld']['opcode']+'0'+regs_binary[i['operands'][0]]+program_dict['variables'][var])
            else:
                print("Undefined Variable")
                x = 1
                break
        else:
                print("General Syntax Error")
                x = 1
                break

    if i['opcode'] == 'st': #for store inst.
        var = i['operands'][1]
        #print(var)
        if len(i['operands'])==2:
            if var in x_l:
                result.append(Instructions['st']['opcode']+'0'+regs_binary[i['operands'][0]]+program_dict['variables'][var])
            else:
                print("Undefined Variable")
                x = 1
                break
        else:
                print("General Syntax Error")
                x =1
                break

    if i['opcode'] == 'div': #for divide inst.
        if i['imm']!= -1 and len(i['operands'])!=2: #immideate error handling done
            print("General Syntax Error")
            x = 1
            break
        elif i['imm'] == -1 and len(i['operands'])==2:
           result.append(Instructions['div']['opcode']+'0'*5+regs_binary[i['operands'][0]]+regs_binary[i['operands'][1]])
        else:
            print("General Syntax Error")
            x = 1
            break
      
    if i['opcode'] == 'ls': #for left shift inst.
        if i['imm'] == -1 and len(i['operands']) == 2: #immideate error handling done
            print("General Syntax Error")
            x = 1
            break
        elif i['imm'] != -1 and len(i['operands'])==1:
            result.append(Instructions['ls']['opcode']+'0'+regs_binary[i['operands'][0]]+i['imm'])
        else:
            print("General Syntax Error")
            x = 1
            break

    if i['opcode'] == 'rs': #for right shift inst.
        if i['imm'] == -1 and len(i['operands']) == 2: #immideate error handling done
            print("General Syntax Error")
            x = 1
            break
        elif i['imm'] != -1 and len(i['operands'])==1:
            result.append(Instructions['rs']['opcode']+'0'+regs_binary[i['operands'][0]]+i['imm'])
        else:
            print("General Syntax Error")
            x = 1
            break

    if i['opcode'] == 'xor': #for xor inst.
        if i['imm']!= -1: #immideate error handling done
              print("General Syntax Error")
              x = 1
              break
        elif i['imm'] == -1 and len(i['operands'])==3:
            result.append(Instructions['xor']['opcode']+'00'+regs_binary[i['operands'][0]]+regs_binary[i['operands'][1]]+regs_binary[i['operands'][2]])
        else:
              print("General Syntax Error")
              x = 1
              break

    if i['opcode'] == 'or': #for or inst.
        if i['imm']!= -1: #immideate error handling done
              print("General Syntax Error")
              x = 1
              break
        elif i['imm'] == -1 and len(i['operands'])==3:
            result.append(Instructions['or']['opcode']+'00'+regs_binary[i['operands'][0]]+regs_binary[i['operands'][1]]+regs_binary[i['operands'][2]])
        else:
              print("General Syntax Error") 
              x=1  
              break

    if i['opcode'] == 'and': #for and inst.
       if i['imm']!= -1: #immideate error handling done
             print("General Syntax Error")
             x=1
             break
       elif i['imm'] == -1 and len(i['operands'])==3:
           result.append(Instructions['and']['opcode']+'00'+regs_binary[i['operands'][0]]+regs_binary[i['operands'][1]]+regs_binary[i['operands'][2]])
       else:
             print("General Syntax Error")
             x=1 
             break

    if i['opcode'] == 'not': #for Invert inst.
        if i['imm']!= -1 and len(i['operands'])!=2: #immideate error handling done
            print("General Syntax Error")
            x=1
            break
        elif i['imm'] == -1 and len(i['operands'])==2:
            result.append(Instructions['not']['opcode']+'0'*5+regs_binary[i['operands'][0]]+regs_binary[i['operands'][1]])
        else:
            print("General Syntax Error")
            x=1 
            break

    if i['opcode'] == 'cmp': #for Compare inst.
        if i['imm']!= -1 and len(i['operands'])!=2: #immideate error handling done
            print("General Syntax Error")
            x=1
            break
        elif i['imm'] == -1 and len(i['operands'])==2:
            result.append(Instructions['cmp']['opcode']+'0'*5+regs_binary[i['operands'][0]]+regs_binary[i['operands'][1]])
        else:
            print("General Syntax Error")
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
                else:
                    x=1

            if x ==1:
                print("Undefined Label")
                break
                    
        else:
                print("General Syntax Error")
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
                else:
                    x=1

            if x ==1:
                print("Undefined Label")
                break

        else:
             print("General Syntax Error")
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
                else:
                    x=1

            if x ==1:
                print("Undefined Label")
                break

        else:
             print("General Syntax Error")
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
                else:
                    x=1

            if x ==1:
                print("Undefined Label")
                break

        else:
             print("General Syntax Error")
             x=1
             break

    if i['opcode'] == 'hlt': #for halt inst.
        result.append(Instructions['hlt']['opcode']+'0'*11)

#print(result)
#print(program_dict)
#if x ==0:
#    for i in result:
#        print(i)

#result.append('1101000000000000')
#st = ''
#if x == 0:
#    for i in result:
#        st += i
#        st += '\n'
#        
#s=len(st)
#st=st[0:s-1]        
#print(st)
#if x == 0:
#    for i in range(len(result)):
#        l = result[i].strip()
#        if i!=len(result)-1:
#            sys.stdout.write(l+'\n')
#        else:
#            sys.stdout.write(l)

if x == 0:
    for i in range(len(result)):
        l = result[i].strip()
        if i!=len(result)-1:
            sys.stdout.write(l+'\n')
        else:
            sys.stdout.write(l)
