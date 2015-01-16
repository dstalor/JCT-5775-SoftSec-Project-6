# from psd_handlers import psd_HandlersFactory
# psd_io = psd_HandlersFactory.hfactory.get_psd_io_handler()

def ask_yes_no(str_prompt):
    answer=""
    while answer not in ["y", "n"]:
        answer=raw_input(str_prompt+" (y/n)")
    return answer


