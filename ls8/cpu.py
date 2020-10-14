"""CPU functionality."""

import sys

if len(sys.argv) != 2:
    print("Usage: missing command line file argument")
    sys.exit(1)

# helper function to convert binary to decimal
def bin_to_int(num):
    return int(str(num))

""" OP Codes """
LDI     = 0b10000010 # LDI register immediate.  Set the value of a register to an integer.
HLT     = 0b00000001 # Halt the CPU (and exit the emulator).
PRN     = 0b01000111 # Print numeric value stored in the given register.


class CPU:
    """Main CPU class."""

    """OP Codes """
  

    def __init__(self):
        """Construct a new CPU."""
        self.ram = 256 * [0]
        self.reg = 8 * [0]
        # self.reg[7] = OxF4
        self.halted = False
        self.pc = 0




    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value
    
    
    def load(self, filename):
        """Open a file and load a program into memory."""
        address = 0

        try:
            with open(filename) as f:
                for line in f:
                    # Split the current line on the # symbol
                    split_line = line.split('#')

                    code_value = split_line[0].strip() # removes whitespace and \n character
                    # Make sure that the value before the # symbol is not empty
                    if code_value == '':
                        continue

                    num = ((int(code_value, 2)))
                    self.ram_write(address, num)
                    # print(num)
                    address += 1
                    

        except FileNotFoundError: 
            print(f"{sys.argv[1]} file not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: pc: %02X | ram: %02X %02X %02X | reg: " % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')
        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    def num_operands(self, instruction):
        """Returns the number of operands (parameters) an instruction takes"""
        return instruction >> 6

    def advance_pc(self, instruction):
        """Returns the number of bytes (lines) to advance the pc given an instruction"""
        return self.num_operands(instruction) + 1

    def run(self):
        """Run the CPU."""
        while self.halted == False:
        # Read line by line from memory
            instruction = self.ram[self.pc]

            if instruction == LDI:
                # takes a register and converts that register value into an integer
                # first number after instruction will be the register number
                reg_num = bin_to_int((self.ram_read(self.pc + 1)))
                # print(f"reg num {reg_num}")
                # second number after instruction will be the integer
                integer = bin_to_int(self.ram_read(self.pc + 2))
                # print(f"integer {integer}")
                self.reg[reg_num] = integer
                self.pc += self.advance_pc(instruction)
                # print(self.trace())

            elif instruction ==  PRN:
                # Print the number in the register
                reg_num = bin_to_int((self.ram_read(self.pc + 1)))
                print(self.reg[reg_num])
                self.pc += self.advance_pc(instruction)
                # print(self.trace())

            elif instruction == HLT:
                halted = False
                self.pc += self.advance_pc(instruction)
                # print(self.trace())
            else:
                # print(self.trace())
                print(f"Unknown instruction {instruction}")
                sys.exit(1)

