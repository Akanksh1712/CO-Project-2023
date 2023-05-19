# CO-Project-2023

The given code is an assembler program written in Python. It reads lines of assembly code and extracts labels, instructions, and variables.

The code defines a dictionary called "Instructions" that maps each instruction mnemonic to its corresponding opcode, number of operands, and addressing modes. It also defines a dictionary called "regs_binary" that maps register names to their binary representation.

The code uses regular expressions to match different patterns in the assembly code. It checks for labels, instructions, and variables using specific patterns.

The code initializes a dictionary called "program_dict" to store labels, instructions, and variables. It iterates over the lines of assembly code and tries to extract information from each line.
