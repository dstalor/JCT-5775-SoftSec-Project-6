from psd_helpers.psd_Helpers import *
from psd_visualizer.psd_Visualizer import *
from psd_analyzer.psd_Analyzer import *
from sys import maxint
import subprocess
import os

class psd_Project:
    def __init__(self, psd, filename=None):
        self.psd = psd
        self.visualizer = psd_Visualizer(self)
        self.analyzer = psd_Analyzer(self)
        self.filename = filename

        if filename != None:
            self.load_executable(filename)

    def load_executable(self, filename):
        if self.analyzer.get_pe() is not None:
            # answer = ask_yes_no("There is already file loaded, overwrite?")
            # if answer is 'n':
            #     print("File not loaded.")
            #     return
            #TODO This print is until we have console-view
            print "There is already file loaded, overwriting"

        self.filename = filename
        # This function loads the file, parse it and creates pefile object from it.
        self.analyzer.load_executable(filename)
        self.visualizer.create_views()

    def run_executable(self):
        if not self.filename:
            print "Can not run because no executable is loaded!"
            return

        temp_filename = ""

        #1. find a temp-name that does not exist already
        #TODO This is temporary for our POC. Ideally we will ask the user for the file name

        for i in xrange(maxint):
            temp_filename = self.filename+"_temp_"+str(i)+".exe"
            if os.path.isfile(temp_filename):
                continue
            else:
                break
        else:
            print "Couldn't find a temp file name."
            return

        print "Creating temporary file: ",temp_filename
        print "Please delete it manually, currently delete mechanizem is not implemented! "

        #2. save executable
        self.save_executable(temp_filename)

        #3. run and wait for it to finish

        # this command should work only under windows
        # http://stackoverflow.com/questions/11585168/launch-an-independent-process-with-python
        os.startfile(temp_filename)

        #try:
        #    subprocess.check_call([temp_filename])
        #except subprocess.CalledProcessError:
        #     pass

        #4. delete file
        #os.remove(temp_filename)

    def save_executable(self, filename):
        if not self.filename:
            print "Can not save because no executable is loaded!"
            return

        pe = self.analyzer.pe
        pe.write(filename)

    def patch_byte_by_rva(self, rva_address, byte_val_str):
        """
        :param rva_address: int, the rva address of the byte to change
        :param byte_val_str: string with the byte value, like "ff" or "01"
        :return:
        """
        if not self.filename:
            print "Can not patch file because no executable is loaded!"
            return

        byte_str = byte_val_str.decode('hex')
        pe = self.analyzer.pe

        #TODO Add here update to disassembly

        pe.set_bytes_at_rva(rva_address, byte_str)

