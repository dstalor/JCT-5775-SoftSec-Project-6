from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
import resources

# from jsHooks import *


class JsHooks(QObject):
    def __init__(self, widget, psd_project, psd_gui):
        QObject.__init__(self)
        self.psd_project = psd_project
        self.visualizer = psd_project.visualizer
        self.psd_gui  = psd_gui
        resources.qInitResources()

    def get_all_html_lines(self):
        return self.visualizer.get_all_html_lines()

    @pyqtSlot(str, result=int)
    def get_line_id_by_address(self, address):
        return self.visualizer.get_line_id_by_address(int(str(address), 16))

    @pyqtSlot(str, str)
    def patch_byte_by_rva(self, rva_address, byte_val_str):
        rva_address_int = int(str(rva_address), 16)
        self.psd_project.patch_byte_by_rva(rva_address_int, str(byte_val_str))

    @pyqtSlot()
    def run_executable(self):
        self.psd_project.run_executable()

    @pyqtSlot()
    def load_executable(self):
        self.psd_gui.load_executable_gui()

    visualizer_lines = pyqtProperty(str, fget=get_all_html_lines)


class psd_EditorGUI(object):
    def __init__(self, psd_project, psd_gui, webview):
        self.psd_gui  = psd_gui
        self.psd_project = psd_project
        self.html = ""
        self.webview = webview
        self.line_count = self.calculate_line_count()
        self.bridge = JsHooks(self.webview, self.psd_project, self.psd_gui)

    def calculate_line_count(self):
        return 100  # TODO: calculate here how many lines there are in the view

    def update_view(self):
        self.set_html()

    def set_html(self):
        with open("psd_GUI/base.html", "r") as myfile:
            self.html = myfile.read()

        self.webview.page().mainFrame().addToJavaScriptWindowObject("pyObj", self.bridge)
        self.webview.setHtml(self.html)