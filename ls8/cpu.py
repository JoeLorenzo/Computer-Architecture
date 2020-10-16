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
CMP     = 0B10100111 # Compare two registers for >, =, or < and sets the fl bits
JMP     = 0b01010100 # Jump to the address stored in the given register.
JEQ     = 0b01010101 # If equal flag is set (true), jump to the address stored in the given register.
JNE     = 0b01010110 # If E flag is clear (false, 0), jump to the address stored in the given register.


class CPU:
    """Main CPU class."""

    """OP Codes """
  

    def __init__(self):
        """Construct a new CPU."""
        self.ram = 256 * [0]
        self.reg = 8 * [0]
        self.halted = False
        self.pc = 0
        self.fl = 0b00000000




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

    
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: pc: %02X | ram: %02X %02X %02X | reg: " % (
            self.pc,
            self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')
        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    
    def get_bin_digits(self, binary_number, start_digit, end_digit=None):
        # a temperary byte that will be used to arrive to the masked byte
        mask_byte = 0b11111111
        # edge case if no ending digit is provided then default to a single digit
        if end_digit == None:
            end_digit = start_digit

        # determines how many shifts to right for the binary number in the parameter
        binary_right_shift = 8 - end_digit
        # print(f"right shift {binary_right_shift}")
        
        # determines how many shfits to the right to create our mask 
        byte_right_shift = start_digit - 1
        # print(f"byte right shift {byte_right_shift}")

        # performs the right shift on the binary number input
        shifted_binary = binary_number >> binary_right_shift
        # print(f"shifted binary {bin(shifted_binary})")

        # creates the mask 
        mask = mask_byte >> byte_right_shift
        # print(f"mask: {bin(mask)}")
        
        # perform & on individual bits to get our digits
        return shifted_binary & mask
         
    
    def num_operands(self, instruction):
        """Returns the number of operands (parameters) an instruction takes"""
        return self.get_bin_digits(instruction, 1, 2)
    
    def advance_pc(self, instruction):
        """Returns the number of bytes (lines) to advance the pc given an instruction"""
        return self.num_operands(instruction) + 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def compare(self, reg_a, reg_b):
        """Compares two registers"""
        # XOR bitwise operation to check if registers are equal
        if ((self.reg[reg_a] ^ self.reg[reg_b]) == 0):
            self.fl = 0b00000001
            # print(f"reg a value {reg_a} is EQUAL to reg b value {self.reg[reg_b]}")
            # print(f"fl: {bin(self.fl)}")

        elif (self.reg[reg_a] > self.reg[reg_b]):
            self.fl = 0b00000010
            # print(f"reg a value {self.reg[reg_a]} is GREATER THEN reg b value {self.reg[reg_b]}")
            # print(f"fl: {bin(self.fl)}")


        elif (self.reg[reg_a] < self.reg[reg_b]):
            self.fl = 0b00000100
            # print(f"reg a value {self.reg[reg_a]} is LESS THEN reg b value {self.reg[reg_b]}")
            # print(f"fl: {bin(self.fl)}")

    def run(self):
        """Run the CPU."""
        while self.halted == False:

            instruction = self.ram[self.pc]

            if instruction == LDI:
                # takes a register and converts that register value into an integer
                # first number after instruction will be the register number
                reg_a = bin_to_int((self.ram_read(self.pc + 1)))
                # print(f"reg num {reg_num}")
                # second number after instruction will be the integer
                integer = bin_to_int(self.ram_read(self.pc + 2))
                # print(f"integer {integer}")
                self.reg[reg_a] = integer
                # print(f"LDI  REG INT: {self.reg[reg_num]} PC {self.pc}")
                self.pc += self.advance_pc(instruction)

            elif instruction ==  PRN:
                # Print the number in the register
                reg_num = bin_to_int((self.ram_read(self.pc + 1)))
                print(self.reg[reg_num])
                # print(f"PRN {self.reg[reg_num]} CURR PC {self.pc}")
                self.pc += self.advance_pc(instruction)

            elif instruction == CMP:
                # gets the value of reg a using the get_bin_digits helper function
                reg_a = self.get_bin_digits(self.ram_read(self.pc+1), 6, 8)
                # print(f"pc +1 {self.ram_read(self.pc+1)}")
                # print(f"reg_a {reg_a}")

                # gets the value of reg b using the get_bin_digits helper function
                reg_b = self.get_bin_digits(self.ram_read(self.pc+2), 6, 8)
                # print(f"pc +2 {self.ram_read(self.pc+2)}")
                # print(f"reg_b {reg_b}")

                # compares the two registers
                self.compare(reg_a, reg_b)
                # print(f"CMP reg a:{reg_a} value {self.reg[reg_a]} reg b:{reg_b} value {self.reg[reg_b]} FL:{bin(self.fl)} PC {self.pc}")
                self.pc += self.advance_pc(instruction)
            
            elif instruction == JMP:
                # gets the value of reg a using the get_bin_digits helper function
                reg_a = self.get_bin_digits(self.ram_read(self.pc+1), 6, 8)
                # print(f"JMP reg a:{reg_a} value:{self.reg[reg_a]} jump to memory address {self.reg[reg_a]}  PC:{self.pc}")
                self.pc = self.reg[reg_a]

            elif instruction == JEQ:
                # gets the value of reg a using the get_bin_digits helper function
                reg_a = self.get_bin_digits(self.ram_read(self.pc+1), 6, 8)
                if self.get_bin_digits(self.fl,8) == 0b1:
                    # print(f"JEQ reg a:{reg_a} value:{self.reg[reg_a]} fl:{bin(self.fl)} EQ flag true jump to pc {self.reg[reg_a]} PC:{self.pc}")
                    self.pc = self.reg[reg_a]
                else: 
                    # print(f"JEQ reg a:{reg_a} value:{self.reg[reg_a]} fl:{bin(self.fl)} EQ flag FALSE, go to the next instruction. PC:{self.pc}")
                    self.pc += self.advance_pc(instruction)
                
            elif instruction == JNE:
                # gets the value of reg a using the get_bin_digits helper function
                reg_a = self.get_bin_digits(self.ram_read(self.pc+1), 6, 8)
                if self.get_bin_digits(self.fl,8) == 0b0:
                    # print(f"JNE reg a:{reg_a} value:{self.reg[reg_a]} fl:{bin(self.fl)} EQ flag False jump to pc {self.reg[reg_a]} PC:{self.pc}")
                    self.pc = self.reg[reg_a]
                else: 
                    # print(f"JNE reg a:{reg_a} value:{self.reg[reg_a]} fl:{bin(self.fl)} EQ flag TRUE go to the next instruction PC:{self.pc}")
                    self.pc += self.advance_pc(instruction)


            elif instruction == HLT:
                halted = False
                self.pc += self.advance_pc(instruction)
                sys.exit(1)
           
            else:
                print(f"Unknown instruction {instruction}")
                sys.exit(1)

