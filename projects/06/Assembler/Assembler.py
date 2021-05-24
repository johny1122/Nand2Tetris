import sys
import re
import os

A_COMMAND = 1  # @XXX
C_COMMAND = 2  # dest=comp;jmp
L_COMMAND = 3  # (XXX)

variables_number = 0
symbol_table = {}


def command_type(command):
    """
    check which type is the current command
    :param command: string of the command
    :return: A_COMMAND - @XXX / C_COMMAND - dest=comp;jmp / L_COMMAND - (XXX)
    """
    if command[0] == "@":
        return A_COMMAND
    if command[0] == "(":
        return L_COMMAND
    else:
        return C_COMMAND


def decimal_to_binary(num):
    """
    translate given decimal number to it's binary value
    :param num: string of decimal number
    :return: string of binary value
    """
    binary = bin(int(num))
    return binary[2:]


def clean_line(line):
    """
    clean the line from spaces, tabs, and comments
    :param line: string of line
    :return: string of clean line
    """
    line = line.replace(" ", "")
    line = line.replace("\t", "")
    line = line.replace("\n", "")
    index_comment = line.find("//")
    if index_comment != -1:  # found comment
        if index_comment == 0:  # all line is just a comment
            line = ""
        else:
            line = line[:index_comment]
    return line


def dest_translate(dest):
    """
    translate dest par of C_COMMAND to it's binary number value
    :param dest: string of dest part of C_COMMAND
    :return: string of binary number of dest command
    """
    all_dest = {
        "null": "000",
        "M": "001",
        "D": "010",
        "MD": "011",
        "A": "100",
        "AM": "101",
        "AD": "110",
        "AMD": "111"
    }
    return all_dest[dest]


def comp_translate(comp):
    """
    translate comp part of C_COMMAND to it's binary number
    :param comp: string of comp command
    :return: string of binary number of the given jump command
    """
    all_comp = {
        # a = 0
        "0": "0101010",
        "1": "0111111",
        "-1": "0111010",
        "D": "0001100",
        "A": "0110000",
        "!D": "0001101",
        "!A": "0110001",
        "-D": "0001111",
        "-A": "0110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "D+A": "0000010",
        "D-A": "0010011",
        "A-D": "0000111",
        "D&A": "0000000",
        "D|A": "0010101",

        # a = 1
        "M": "1110000",
        "!M": "1110001",
        "-M": "1110011",
        "M+1": "1110111",
        "M-1": "1110010",
        "D+M": "1000010",
        "D-M": "1010011",
        "M-D": "1000111",
        "D&M": "1000000",
        "D|M": "1010101",

        # special (multiplication and shift)
        "D*A": "110000",
        "D*M": "110100",
        "D<<": "101011",
        "A<<": "101010",
        "M<<": "101110",
        "D>>": "101001",
        "A>>": "101000",
        "M>>": "101100"
    }
    return all_comp[comp]


def comp_is_shift_or_mult(comp):
    """
    check if comp command is special (multiplication and shift) or not
    :param comp: string of comp command
    :return: True if yes and False if not
    """
    if comp == "D*A" or comp == "D*M" or comp == "D<<" or comp == "A<<" or comp == "M<<" or comp == "D>>" or \
       comp == "A>>" or comp == "M>>":
        return True
    return False


def jump_translate(jump):
    """
    translate jump part of C_COMMAND
    :param jump: string of jump part
    :return: string of binary number of the given jump command
    """
    all_jump = {
        "null": "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111"
    }
    return all_jump[jump]


def a_command_to_binary(command):
    """
    translate A_COMMAND to it's binary value
    :param command: the A_COMMAND
    :return: string of binary value of A_COMMAND
    """
    global variables_number

    clean_command = command[1:]
    if not clean_command.isnumeric():  # if XXX is a variable
        if clean_command not in symbol_table:
            symbol_table[clean_command] = variables_number
            variables_number += 1
        binary_result = decimal_to_binary(symbol_table[clean_command])
    else:  # XXX is a number
        binary_result = decimal_to_binary(clean_command)
    return "0" + ("0" * (15 - len(binary_result))) + binary_result


def c_command_to_binary(command):
    """
    translate C_COMMAND to it's binary value
    :param command: the C_COMMAND
    :return: string of binary value of C_COMMAND
    """
    command_list = re.split("[=;]", command)
    if "=" in command:
        dest_command = command_list[0]
        comp_command = command_list[1]
        if len(command_list) == 3:  # there are all 3 parts of C_COMMAND
            jump_command = command_list[2]
        else:  # there is no jump part
            jump_command = "null"
    elif ";" in command:  # command has the pattern: comp;jmp
        comp_command = command_list[0]
        jump_command = command_list[1]
        dest_command = "null"
    else:  # command has the pattern: comp (shift or mult)
        comp_command = command_list[0]
        jump_command = "null"
        dest_command = "null"

    dest_binary = dest_translate(dest_command)
    comp_binary = comp_translate(comp_command)
    jump_binary = jump_translate(jump_command)

    if comp_is_shift_or_mult(comp_command):
        return comp_binary + "0000" + dest_binary + jump_binary
    return "111" + comp_binary + dest_binary + jump_binary


def l_command_to_binary(command):
    """
    translate L_COMMAND to its saved value in symbol_table
    :param command: the L_COMMAND string
    :return: string of binary value of L_COMMAND
    """
    return decimal_to_binary(symbol_table[command[1:-1]])


def first_pass(line_list):
    """
    first pass of the file. just insert all the labels to the symbol_table
    :param line_list: list of all the lines
    :return: none
    """
    line_number = 0
    for line in line_list:
        curr_line = clean_line(line)
        if curr_line == "":
            continue
        if command_type(curr_line) != L_COMMAND:
            line_number += 1
        else:
            symbol_table[curr_line[1:-1]] = line_number


def second_pass(list_line, hack_file):
    """
    second pass of the file. read line by line and write the correct binary
    number to the hack_file
    :param list_line: list of all the lines
    :param hack_file: output file
    :return: none
    """
    for line in list_line:
        curr_line = clean_line(line)
        if curr_line == "":
            continue
        comm_type = command_type(curr_line)
        line_in_binary = ""
        if comm_type == A_COMMAND:
            line_in_binary = a_command_to_binary(curr_line)
        elif comm_type == C_COMMAND:
            line_in_binary = c_command_to_binary(curr_line)
        elif comm_type == L_COMMAND:  # L_COMMAND should be ignored
            continue

        hack_file.write(line_in_binary + "\n")


def initialize_globals():
    """
    initialize the globals variables_number and symbol_table to the default at the beginning of each
    file translation
    :return: none
    """
    global variables_number
    global symbol_table
    variables_number = 16  # start insert variables from place 16
    symbol_table = dict(R0=0, R1=1, R2=2, R3=3, R4=4, R5=5, R6=6, R7=7, R8=8,
                        R9=9, R10=10, R11=11, R12=12, R13=13, R14=14, R15=15,
                        SP=0, LCL=1, ARG=2, THIS=3, THAT=4,
                        SCREEN=16384, KBD=24576)  # reset to default symbol_table


def main():
    arg_string = os.path.abspath(sys.argv[1])
    if not os.path.exists(arg_string):
        print("USAGE: file not found")
        sys.exit(1)
    asm_files_list = []
    if os.path.isdir(arg_string):  # if argument is directory
        for file in os.listdir(arg_string):
            if file.endswith(".asm"):
                if os.name == 'nt':  # if on windows
                    asm_files_list.append(arg_string + '\\' + file)
                else:  # if on linux
                    asm_files_list.append(arg_string + '/' + file)
    else:  # argument is file
        if not sys.argv[1].endswith('.asm'):
            print("USAGE: unsupported file type")
            sys.exit(1)
        else:  # if argument is an asm file
            asm_files_list.append(arg_string)

    for asm_address in asm_files_list:
        initialize_globals()
        asm_file = open(asm_address, "r")
        line_list = asm_file.readlines()
        first_pass(line_list)

        name = asm_address.split(".asm")[0] + ".hack"
        hack_file = open(name, "w")

        second_pass(line_list, hack_file)

        hack_file.close()
    return


if __name__ == "__main__":
    main()
