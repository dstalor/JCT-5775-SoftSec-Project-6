import string
import re
from capstone.x86 import *

#jump_instructions = ['call','jmp', 'jo', 'jno', 'js', 'jns', 'je', 'jz', 'jne', 'jnz', 'jb', 'jnae', 'jc', 'jnb', 'jae', 'jnc', 'jbe', 'jna', 'ja', 'jnbe', 'jl', 'jnge', 'jge', 'jnl', 'jle', 'jng', 'jg', 'jnle', 'jp', 'jpe', 'jnp', 'jpo', 'jcxz', 'jecxz']

def ask_yes_no(str_prompt):
    answer=""
    while answer not in ["y", "n"]:
        answer=raw_input(str_prompt+" (y/n)")
    return answer

def strip_non_printable(dirty_str):
    """
    :param str: string to stripped out of non printable bytes
    :return: returns string that conatins only printable bytes
    """
    return ''.join(filter(string.printable.__contains__, dirty_str))

#def is_jmp_instruction(nemonic_str):
#    return  nemonic_str in jump_instructions

#this one is from stackoverflow: http://stackoverflow.com/questions/11592261/check-if-string-is-hexadecimal
def is_hex(str):
    try:
        int(str, 16)
        return True
    except ValueError:
        return False

def is_ptr(str):
    return "ptr" in str

def is_dword_ptr(str):
    return "dword ptr" in str

def get_hexes_in_str(str):
    hex_pattern = r'(0x[0-9a-fA-F]+)'
    return re.findall(hex_pattern, str)

#TODO move this to analyzer
def get_constants(code_line):
        """
        :param code_line: capstone instruction
        :return: list of constants
        """
        constants = []
        for op in code_line.operands:
            if op.type == X86_OP_MEM:
                if op.mem.disp != 0:
                    constants.append(int(op.mem.disp))
            elif op.type == X86_OP_IMM:
                constants.append(int(op.imm))
        return constants