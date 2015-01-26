import sys
import resources
from PyQt4 import QtGui, QtWebKit
from PyQt4.QtCore import *

class JsHooks(QObject):
    def __init__(self, psd, psd_gui):
        QObject.__init__(self)
        self.psd_project = psd.psd_project
        self.visualizer = self.psd_project.visualizer
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

    @pyqtSlot(result=str)
    def get_all_html_empty_lines(self):
        return self.visualizer.get_all_html_empty_lines()

    @pyqtSlot(str, result=str)
    def get_html_line(self, lineid_str):
        line_id = int(lineid_str)
        return self.visualizer.get_html_line(line_id)

    @pyqtSlot(str, str, result=str)
    def get_html_lines(self, start_lineid_str, end_lineid_str):
        linerange = (int(start_lineid_str), int(end_lineid_str))
        return self.visualizer.get_html_lines(linerange)
    
    visualizer_lines = pyqtProperty(str, fget=get_all_html_lines)

class psd_GUI(object):
    def __init__(self, psd):
        self.psd = psd
        self.editor_view = None
        self.main_window = None
        resources.qInitResources()
        self.app = QtGui.QApplication(sys.argv)
        self.bridge  = JsHooks(self.psd, self)

    def get_filename_dialog(self):
        dialog = QtGui.QFileDialog()
        filename = QtGui.QFileDialog.getOpenFileName(dialog)
        return str(filename)

    def load_executable_gui(self):
        filename = self.get_filename_dialog()
        self.psd.psd_project.load_executable(filename)
    #    self.editor_view.update_view()

    def create_main_window(self):
        self.main_window = QtGui.QMainWindow()

    def create_main_view(self):
        webview = QtWebKit.QWebView()
        webview.setContextMenuPolicy(Qt.NoContextMenu)
        self.main_view = webview
        self.main_window.setCentralWidget(self.main_view)
        with open("psd_GUI/base.html", "r") as myfile:
            self.html = myfile.read()

        self.main_view.page().mainFrame().addToJavaScriptWindowObject("pyObj", self.bridge)
        self.main_view.setHtml(self.html)

    def run(self):
        self.create_main_window()
        self.create_main_view()

        self.main_window.showMaximized()
        self.main_window.activateWindow()

        sys.exit(self.app.exec_())
