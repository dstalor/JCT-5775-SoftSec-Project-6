import sys
from PyQt4 import QtCore, QtGui, QtWebKit
from psdEditorGUI import *
from psd import *


class psdGUI(object):
    def __init__(self, psd):
        self.psd = psd
        self.editor_view = None
        self.main_window = None
        resources.qInitResources()

    def create_main_window(self):
        self.main_window = QtGui.QMainWindow()

    def create_editor_view(self, psd_project):
        webview = QtWebKit.QWebView()
        webview.setContextMenuPolicy(Qt.NoContextMenu)
        self.editor_view = psdEditorGUI(psd_project, webview)
        self.main_window.setCentralWidget(webview)

    def run(self):
        app = QtGui.QApplication(sys.argv)

        self.create_main_window()

        self.create_editor_view(self.psd.psd_project)

        self.editor_view.update_view()

        self.main_window.show()

        sys.exit(app.exec_())

# if __name__ == '__main__':
# psd_main = psd()
#     psd_main.create_new_project("examples\\helloworld.exe")
#     psd_GUI = psdGUI(psd_main)
