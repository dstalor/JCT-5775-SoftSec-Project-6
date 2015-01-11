from PyQt4 import QtCore, QtGui, QtWebKit

class psdEditorGUI(object):
    def __init__(self, psd_project, webview):
        self.psd_project = psd_project
        self.html = ""
        self.webview = webview
        self.line_count = self.calculate_line_count()

    def calculate_line_count(self):
        return 100 # to-do: calculate here how much lines there are in the view

    def update_view(self):
        self.set_html_body(self.psd_project.visualizer.get_all_lines())

    def set_html(self, str):
        self.html = str
        self.webview.setHtml(self.html)

    def set_html_body(self, str):
        new_html = """
        <head>
            <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
            <style>
            pre {
                font-weight: bold;
            }
            .row-header {
                color: #008080;
            }
            .byte-data {
                color: #000080;
            }
            .spaceafter {
                margin-right: 8px;
            }
            .final {
                margin-right: 16px;
            }
            .highlight {
                background-color: yellow;
            }
            </style>
            <script>
            $(document).ready(function () {
                $("span.byte-data").click(function() {
                    $( this ).toggleClass( "highlight" );
                });
            });
            </script>
        </head>
        """+"<html><body><pre>"+str+"</pre></body></html>"
        self.set_html(new_html)
