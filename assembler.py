import sys

# Dictionaries for translation
dest_dict = {
    None: '000',
    'M': '001',
    'D': '010',
    'MD': '011',
    'A': '100',
    'AM': '101',
    'AD': '110',
    'AMD': '111'
}

comp_dict = {
    '0': '0101010',
    '1': '0111111',
    '-1': '0111010',
    'D': '0001100',
    'A': '0110000',
    '!D': '0001101',
    '!A': '0110001',
    '-D': '0001111',
    '-A': '0110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'D+A': '0000010',
    'D-A': '0010011',
    'A-D': '0000111',
    'D&A': '0000000',
    'D|A': '0010101',
    'M': '1110000',
    '!M': '1110001',
    '-M': '1110011',
    'M+1': '1110111',
    'M-1': '1110010',
    'D+M': '1000010',
    'D-M': '1010011',
    'M-D': '1000111',
    'D&M': '1000000',
    'D|M': '1010101'
}

jump_dict = {
    None: '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111'
}

# Symbol table (predefined and dynamic)
symbol_table = {
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SCREEN': 16384,
    'KBD': 24576
}

next_variable_address = 16

# clean and parse lines
def clean_lines(lines):
    cleaned_lines = []
    for line in lines:
        # Remove comments and whitespace
        line = line.split('//')[0].strip()
        if line:  # Ignore empty lines
            cleaned_lines.append(line)
    return cleaned_lines

def commandType(command):
    if command.startswith('@'):
        return "A_COMMAND"
    elif command.startswith('(') and command.endswith(')'):
        return "L_COMMAND"
    else:
        return "C_COMMAND"

def getSymbol(command):
    if commandType(command) == "A_COMMAND":
        return command[1:]
    elif commandType(command) == "L_COMMAND":
        return command[1:-1]
    return None

def getDest(command):
    if '=' in command:
        return command.split('=')[0]
    return None

# extract comp mnemonic from C command
def getComp(command):
    if '=' in command:
        command = command.split('=')[1]
    if ';' in command:
        command = command.split(';')[0]
    return command

# extract jump mnemonic from C command
def getJump(command):
    if ';' in command:
        return command.split(';')[1]
    return None

def dest2bin(mnemonic):
    return dest_dict.get(mnemonic, '000')

def comp2bin(mnemonic):
    return comp_dict.get(mnemonic, '0000000')

def jump2bin(mnemonic):
    return jump_dict.get(mnemonic, '000')

def processA(line, lineNo):
    global next_variable_address
    symbol = getSymbol(line)
    if symbol.isdigit():  # if number
        address = int(symbol)
    else:  # if symbol
        if symbol not in symbol_table:
            symbol_table[symbol] = next_variable_address
            next_variable_address += 1
        address = symbol_table[symbol]
    return '0' + format(address, '015b')

# process C-commands
def processC(line):
    dest = getDest(line)
    comp = getComp(line)
    jump = getJump(line)
    return '111' + comp2bin(comp) + dest2bin(dest) + jump2bin(jump)

# Function to process L-commands
def processL(line, lineNo):
    symbol = getSymbol(line)
    if symbol not in symbol_table:
        symbol_table[symbol] = lineNo

# First pass: Build symbol table
def pass_1(file):
    cleaned_lines = clean_lines(file)
    lineNo = 0
    for line in cleaned_lines:
        if commandType(line) == "L_COMMAND":
            processL(line, lineNo)
        else:
            lineNo += 1

# Second pass: Generate binary code
def pass_2(file):
    cleaned_lines = clean_lines(file)
    binary_output = []
    for line in cleaned_lines:
        cmd_type = commandType(line)
        if cmd_type == "A_COMMAND":
            binary_output.append(processA(line, 0))  # lineNo not needed for A-commands
        elif cmd_type == "C_COMMAND":
            binary_output.append(processC(line))
        elif cmd_type == "L_COMMAND":
            pass  # Labels are already processed in pass_1
    return binary_output

# Main function to assemble the file
def assemble_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("File not found.")
        return

    # First pass: Build symbol table
    pass_1(lines)

    # Second pass: Generate binary code
    binary_output = pass_2(lines)

    # Write binary output to a file
    output_filename = filename.replace('.asm', '.hack')
    with open(output_filename, 'w') as output_file:
        for binary in binary_output:
            output_file.write(binary + '\n')

    print(f"Assembly completed. Output written to {output_filename}")

# Entry point
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python assembler.py <filename.asm>")
    else:
        assemble_file(sys.argv[1])