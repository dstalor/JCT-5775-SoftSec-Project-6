from psd_helpers.psd_Helpers import *
from psd_visualizer.psd_Visualizer import *
from psd_analyzer.psd_Analyzer import *

# from psd_handlers import psd_HandlersFactory
# psd_io = psd_HandlersFactory.hfactory.get_psd_io_handler()

class psd_Project:
    def __init__(self, psd, filename = None):
        self.psd=psd
        self.visualizer = psd_Visualizer(self)
        self.analyzer = psd_Analyzer(self)

        if filename is None:
            filename = raw_input("please enter executable file name to open: ")

        self.load_executable(filename)

    def load_executable(self, filename):
        if self.analyzer.get_pe() is not None:
            answer = ask_yes_no("There is already file loaded, overwrite?")
            if answer is 'n':
                print("File not loaded.")
                return

        # This function loads the file, parse it and creates pefile object from it.
        self.analyzer.load_executable(filename)
        self.visualizer.create_views()

    def run_executable(self):
        raise NotImplementedError()

