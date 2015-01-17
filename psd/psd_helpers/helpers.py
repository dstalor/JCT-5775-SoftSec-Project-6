import string

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
