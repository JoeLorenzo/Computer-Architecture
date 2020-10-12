"""CPU functionality."""

import sys

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
        self.running = True
        self.pc = 0




    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value
    
    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

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

    def run(self):
        """Run the CPU."""
        while self.running:
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
                self.pc += 3
                # print(self.trace())

            elif instruction ==  PRN:
                # Print the number in the register
                reg_num = bin_to_int((self.ram_read(self.pc + 1)))
                print(self.reg[reg_num])
                self.pc += 2
                # print(self.trace())

            elif instruction == HLT:
                running = False
                self.pc += 1
                # print(self.trace())
            else:
                # print(self.trace())
                print(f"Unknown instruction {instruction}")
                sys.exit(1)

