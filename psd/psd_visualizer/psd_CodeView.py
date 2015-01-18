import math
from psd_visualizer.psd_View import psd_View

__author__ = 'Noam'


class psd_CodeView(psd_View):
    def __init__(self, pe, memory_range):
        super(psd_CodeView, self).__init__(pe, memory_range)
        self._code_lines = memory_range.get_memory_range_metadata().get_code_lines()

    def calculate_line_count(self):
        if not self._code_lines:
            return 0
        else:
            return len(self._code_lines)

    def get_html_lines(self, line_range_tup):
        intersect_lines = self.get_lines_intersection(line_range_tup)
        if not intersect_lines:
            return ""

        (line_start, line_end) = self.absolute_lines_to_relative(intersect_lines)

        str_out = ""
        for l_idx in range(line_start, line_end):
            line = self._code_lines[l_idx]
            str_out += self.html_line(line)

        return str_out

    def html_line(self, line):
        str_rowheader = self.html_rowheader(self._memory_range_metadata.get_range_name(), line.address)
        str_opcode = self.html_opcode(line.mnemonic)
        str_operands = self.html_operands(line.op_str)

        return str_rowheader + str_opcode + str_operands + "\n"

    def html_rowheader(self, rangename, address):
        return "<span class=\"codeview-row-header\">{0: >10} 0x{1:08x}: </span>".format(rangename, address)

    def html_opcode(self, mnemonic):
        return "<span class=\"codeview-opcode spaceafter\">{0: <5}</span>".format(mnemonic)

    def html_operands(self, op_str):
        return "<span class=\"codeview-param\" >{0}</span>".format(op_str)
