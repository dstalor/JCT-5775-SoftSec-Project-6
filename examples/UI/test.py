import sys  
from PyQt4 import QtCore, QtGui, QtWebKit  
  
"""Html snippet."""  
html = """ 
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
<html>
	<body>
		<pre><span class="row-header">0x00000:</span><span id="00000-data" class="byte-data">4D</span><span id="00001-data" class="byte-data spaceafter">5A</span><span id="00002-data" class="byte-data">74</span><span id="00003-data" class="byte-data spaceafter">00</span><span id="00004-data" class="byte-data">B8</span><span id="00005-data" class="byte-data spaceafter">00</span><span id="00006-data" class="byte-data">00</span><span id="00007-data" class="byte-data spaceafter">00</span><span id="00008-data" class="byte-data">26</span><span id="00009-data" class="byte-data spaceafter">04</span><span id="0000A-data" class="byte-data">01</span><span id="0000B-data" class="byte-data spaceafter">00</span><span id="0000C-data" class="byte-data">FF</span><span id="0000D-data" class="byte-data spaceafter">FF</span><span id="0000E-data" class="byte-data">00</span><span id="0000F-data" class="byte-data final">00</span><span id="00000-ascii" class="byte-ascii">&#77;</span><span id="00001-ascii" class="byte-ascii">&#90;</span><span id="00002-ascii" class="byte-ascii">&#116;</span><span id="00003-ascii" class="byte-ascii">&#46;</span><span id="00004-ascii" class="byte-ascii">&#184;</span><span id="00005-ascii" class="byte-ascii">&#46;</span><span id="00006-ascii" class="byte-ascii">&#46;</span><span id="00007-ascii" class="byte-ascii">&#46;</span><span id="00008-ascii" class="byte-ascii">&#38;</span><span id="00009-ascii" class="byte-ascii">&#46;</span><span id="0000A-ascii" class="byte-ascii">&#46;</span><span id="0000B-ascii" class="byte-ascii">&#46;</span><span id="0000C-ascii" class="byte-ascii">&#255;</span><span id="0000D-ascii" class="byte-ascii">&#255;</span><span id="0000E-ascii" class="byte-ascii">&#46;</span><span id="0000F-ascii" class="byte-ascii">&#46;</span></pre>
	</body>
</html>
"""  
  
class StupidClass(QtCore.QObject):  
    """Simple class with one slot and one read-only property."""  
 
    @QtCore.pyqtSlot(str)  
    def showMessage(self, msg):  
        """Open a message box and display the specified message."""  
        QtGui.QMessageBox.information(None, "Info", msg)  
  
    def _pyVersion(self):  
        """Return the Python version."""  
        return sys.version  
  
    """Python interpreter version property."""  
    pyVersion = QtCore.pyqtProperty(str, fget=_pyVersion)  
  
def main():  
    app = QtGui.QApplication(sys.argv)  
  
    myObj = StupidClass()  
    
    webView = QtWebKit.QWebView()  
    # Make myObj exposed as JavaScript object named 'pyObj'  
    webView.page().mainFrame().addToJavaScriptWindowObject("pyObj", myObj)  
    webView.setHtml(html)  
  
    window = QtGui.QMainWindow()  
    window.setCentralWidget(webView)  
    window.show()  
  
    sys.exit(app.exec_())  
  
if __name__ == "__main__":  
    main()  