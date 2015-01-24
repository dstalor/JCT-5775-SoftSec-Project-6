from psd_helpers.psd_Helpers import *
from psd_visualizer.psd_Visualizer import *
from psd_analyzer.psd_Analyzer import *
from sys import maxint, path
import subprocess

# from psd_handlers import psd_HandlersFactory
# psd_io = psd_HandlersFactory.hfactory.get_psd_io_handler()

class psd_Project:
    def __init__(self, psd, filename=""):
        self.psd = psd
        self.visualizer = psd_Visualizer(self)
        self.analyzer = psd_Analyzer(self)
        self.filename = filename

        if filename != "":
            self.load_executable(filename)



    def load_executable(self, filename):
        if self.analyzer.get_pe() is not None:
            answer = ask_yes_no("There is already file loaded, overwrite?")
            if answer is 'n':
                print("File not loaded.")
                return

        self.filename = filename
        # This function loads the file, parse it and creates pefile object from it.
        self.analyzer.load_executable(filename)
        self.visualizer.create_views()

    def run_executable(self):
        temp_filename = ""
        #1. find a temp-name that does not exist already
        for i in range(maxint):
            temp_filename = self.filename+"_temp_"+str(i)
            if path.isfile(temp_filename):
                continue
            else:
                break

        if i == (maxint-1):
            print "Coudn't find a temp file name."
            return

        #2. save executable
        self.save_executable(temp_filename)

        #3. run
        subprocess.call([temp_filename])

        #4. delete file


    def save_executable(self, filename):
        pe = self.analyzer.pe
        pe.write(filename)


