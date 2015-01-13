from PyQt4 import QtCore, QtGui, QtWebKit

class psdEditorGUI(object):
    def __init__(self, psd_project, webview):
        self.psd_project = psd_project
        self.html = ""
        self.webview = webview
        self.line_count = self.calculate_line_count()
        webview.page().mainFrame().addToJavaScriptWindowObject("pyObj", self.psd_project.visualizer)

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
        	/* Data hex view */
        	.datahex-row-header {
        		color: #008080;
        	}
        	.datahex-byte-data {
        		color: #000080;
        	}
        	.datahex-byte-ascii {
        		color: #000000;
        	}
        	/* Data view */
        	.dataview-row-header {
        		color: #848484;
        		margin-right: 8px;
        	}
        	.dataview-label, .dataview-length {
        		color: #000080;
        		margin-right: 8px;
        	}
        	.dataview-data {
        		color: #008000;
        	}
        	/* Code view */
        	.codeview-row-header {
        		color: #000000;
        		margin-right: 8px;
        	}
        	.codeview-opcode, .codeview-param {
        		color: #000080;
        	}
        	.codeview-constant {
        		color: #008000;
        	}
        	/* Spacing */
        	.spaceafter {
        		margin-right: 8px;
        	}
        	.doublespaceafter {
        		margin-right: 16px;
        	}
        	.fourspacesafter {
        		margin-right: 48px;
        	}
        	
        	.highlight {
        		background-color: yellow;
        	}
        	</style>
        	<script>
        	$(document).ready(function () {
        		$("span.datahex-byte-data").click(function() {
        			$( this ).toggleClass( "highlight" );
        		});
        	});
        	$(document).ready(function () {
        		$("span.codeview-constant").click(function() {
        			$( this ).text(function(i,origText){
        				if (origText.slice(-1) == 'h') {
        					return (hex2bin(origText.substr(0, origText.length - 1)) + 'b');
        				}
        				else if (origText.slice(-1) == 'b'){
        					return (bin2dec(origText.substr(0, origText.length - 1)));
        				}
        				else {
        					return (dec2hex(origText) + 'h');
        				}
        			});
        		});
        		$("#button").click(function() {
        			$("#main").text(function(i,origText){
        				return pyObj.get_all_lines();
        			});
				)};
        	});
        	/**
        	* Convert From/To Binary/Decimal/Hexadecimal in JavaScript
        	* https://gist.github.com/faisalman
        	*
        	* Copyright 2012, Faisalman <fyzlman@gmail.com>
        	* Licensed under The MIT License
        	* http://www.opensource.org/licenses/mit-license
        	*/
        	 
        	(function(){
        	 
        		var convertBase = function (num) {
        			this.from = function (baseFrom) {
        				this.to = function (baseTo) {
        					return parseInt(num, baseFrom).toString(baseTo);
        				};
        				return this;
        			};
        			return this;
        		};
        			
        		// binary to decimal
        		this.bin2dec = function (num) {
        			return convertBase(num).from(2).to(10);
        		};
        		
        		// binary to hexadecimal
        		this.bin2hex = function (num) {
        			return convertBase(num).from(2).to(16);
        		};
        		
        		// decimal to binary
        		this.dec2bin = function (num) {
        			return convertBase(num).from(10).to(2);
        		};
        		
        		// decimal to hexadecimal
        		this.dec2hex = function (num) {
        			return convertBase(num).from(10).to(16);
        		};
        		
        		// hexadecimal to binary
        		this.hex2bin = function (num) {
        			return convertBase(num).from(16).to(2);
        		};
        		
        		// hexadecimal to decimal
        		this.hex2dec = function (num) {
        			return convertBase(num).from(16).to(10);
        		};
        		
        		return this;        
        	})();
        	</script>
        </head>
        """+"<html><body><button type='button' id='button'>Click Me!</button><pre id='main'></pre></body></html>"
        self.set_html(new_html)
