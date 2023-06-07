The following is the ISA description for the Bonus Instruction:

Opcode: 10001
Instruction: Multiply with immediate
Semantics: This instruction performs the computation reg1 = reg1 x imm. If the computation overflows, the overflow flag is set, and 0 is written in reg1.
Syntax: muli reg1 $imm
Type: B

Opcode: 10010
Instruction: Divide with immediate
Semantics: This instruction performs the computation reg1 = reg1 / imm. If the computation overflows, the overflow flag is set, and 0 is written in reg1.
Syntax: divi reg1 $imm
Type: B

Opcode: 10011
Instruction: Compare with immediate
Semantics: This instruction compares reg1 and imm and sets the FLAGS register accordingly.
Syntax: cmpi reg1 $imm
Type: B

Opcode: 10100
Instruction: Exchange registers
Semantics: This instruction exchanges the contents of reg1 and reg2.
Syntax: ex reg1 reg2
Type: C

Opcode: 10101
Instruction: Add with immediate
Semantics: This instruction performs the computation reg1 = reg1 + imm. If the computation overflows, the overflow flag is set, and 0 is written in reg1.
Syntax: addi reg1 $imm
Type: B

Note: Instructions labeled with Type "B" are basic instructions, while the instruction labeled with Type "C" is a control instruction.
