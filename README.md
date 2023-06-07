# CO-Project-2023

For Assembler:
The provided code represents a sophisticated assembler program implemented in Python. Its purpose is to parse lines of assembly code, extracting essential components such as labels, instructions, and variables.

The code includes a meticulously constructed dictionary, named "Instructions," which serves as a mapping between instruction mnemonics and their corresponding opcodes, the number of operands, and the addressing modes associated with each instruction. Additionally, it encompasses a supplementary dictionary called "regs_binary," which facilitates the conversion of register names into their respective binary representations.

To analyze the assembly code, regular expressions are skillfully employed to identify distinct patterns. These patterns are specifically designed to detect labels, instructions, and variables within the code.

Moreover, the code initiates a highly efficient dictionary called "program_dict" to store essential information, including labels, instructions, and variables. It diligently traverses each line of the assembly code, extracting and organizing the pertinent details.

To ensure impeccable performance and enhanced user experience, the assembler has been further augmented with robust error handling capabilities. This noteworthy addition enables the prompt detection and appropriate reporting of any encountered errors.

The code has been ingeniously enhanced to accommodate floating point numbers as well. It now caters to a comprehensive range of floating point numbers, with the upper limit set at 31.5. Furthermore, the assembler effectively verifies the validity of floating point numbers, raising an error message whenever a floating point number is outside the permissible range. Notably, the floating point numbers adhere to a specific format, encompassing the absence of a sign bit, three bits for the exponent, and five bits for the mantissa.

Overall, the code showcases meticulous attention to detail, robust error handling, and comprehensive support for floating point numbers, culminating in a highly professional and advanced assembler program.

For Simulator: 
The code defines a set of instructions and their corresponding operations. It initializes global variables such as `register_file`, `mem`, `PC`, and `flag_val`, which are used to store the state of the simulated system.

The register_file dictionary contains all the registers and their values. The mem dictionary has been created to take the instructions from the stdin  and save them line by line.

there are some defined functions like dtb(decimal  to binary),btd(binary to decimal), ftb(float to binary), btf(binary to float), etc, to make the code more compact and efficient.

The code then reads instructions from mem dictionary and then executes them .The opcode of each instruction has been used to determine the respective working of the instruction. The code includes various instructions such as arithmetic operations (addition, subtraction, multiplication, division), logical operations (AND, OR, XOR), memory operations (load, store), register operations (move, exchange), and more.'
