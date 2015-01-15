from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
import resources

# from jsHooks import *


class JsHooks(QObject):
    def __init__(self, widget, visualizer):
        QObject.__init__(self)
        self.visualizer = visualizer
        resources.qInitResources()

    def get_all_lines(self):
        return self.visualizer.get_all_lines()

    visualizer_lines = pyqtProperty(str, fget=get_all_lines)


class psdEditorGUI(object):
    def __init__(self, psd_project, webview):
        self.psd_project = psd_project
        self.html = ""
        self.webview = webview
        self.line_count = self.calculate_line_count()
        self.bridge = JsHooks(webview, psd_project.visualizer)

    def calculate_line_count(self):
        return 100  # TODO: calculate here how much lines there are in the view

    def update_view(self):
        self.set_html()

    def set_html(self):
        with open("GUI/base.html", "r") as myfile:
            self.html = myfile.read()

        self.webview.page().mainFrame().addToJavaScriptWindowObject("pyObj", self.bridge)
        self.webview.setHtml(self.html)