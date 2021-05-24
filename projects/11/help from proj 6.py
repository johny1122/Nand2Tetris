#%%
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

    #  print("C_COMMAND pars: ", command_list)

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


