import sys

from PyQt4 import QtGui, QtWebKit

from psdEditorGUI import *


class psdGUI(object):
    def __init__(self, psd):
        self.psd = psd
        self.editor_view = None
        self.main_window = None
        resources.qInitResources()
        self.app = QtGui.QApplication(sys.argv)

    def get_filename(self):
        dialog = QtGui.QFileDialog()
        filename = QtGui.QFileDialog.getOpenFileName(dialog)
        return filename

    def create_main_window(self):
        self.main_window = QtGui.QMainWindow()

    def create_editor_view(self, psd_project):
        webview = QtWebKit.QWebView()
        webview.setContextMenuPolicy(Qt.NoContextMenu)
        self.editor_view = psdEditorGUI(psd_project, webview)
        self.main_window.setCentralWidget(webview)

    def run(self):
        self.create_main_window()

        self.create_editor_view(self.psd.psd_project)

        self.editor_view.update_view()

        self.main_window.showMaximized()
        self.main_window.activateWindow()

        sys.exit(self.app.exec_())

# if __name__ == '__main__':
# psd_main = psd()
# psd_main.create_new_project("examples\\helloworld.exe")
# psd_GUI = psdGUI(psd_main)
