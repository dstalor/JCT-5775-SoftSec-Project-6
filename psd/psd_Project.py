from pefile.pefile import PE
from helpers import *
# from psd_handlers import psd_HandlersFactory
# psd_io = psd_HandlersFactory.hfactory.get_psd_io_handler()

class psd_Project:
    def __init__(self, psd, filename = None):
        self.psd=psd
        self.pe = None

        if filename is None:
            filename = raw_input("please enter executable file name to open: ")

        self.load_executable(filename)

    def load_executable(self, filename):

        if self.pe is not None:
            answer = ask_yes_no("There is already file loaded, overwrite?")
            if answer is 'n':
                psd_io.psd_print("File not loaded.")
                return

        # This function loads the file, parse it and creates pefile object from it.
        self.pe = PE(filename)

	def run_executable(self):
		raise NotImplementedError()
