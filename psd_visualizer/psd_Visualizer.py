from psd_HexView import psd_HexView
from psd_CodeView import psd_CodeView
from psd_HeaderView import psd_HeaderView
from psd_HTMLGenerator import *
from psd_AddressViewRangeMap import psd_AddressViewRangeMap
from psd_AddressViewRangeMapList import psd_AddressViewRangeMapList
import math
#TODO: This class should be changed by desgin to represent a collaction of views combined to one linear view
class psd_Visualizer:
    def __init__(self, psd_project):
        self.psd_project = psd_project
        self.addressview_rangemap_list = psd_AddressViewRangeMapList()
        self.psd_html_generator = psd_HTMLGenerator()
        self.linechunk_size = 100

    def add_view(self, addressrange, view):
        self.addressview_rangemap_list.add_range_map(psd_AddressViewRangeMap(addressrange, view))

    def add_hexview(self, memory_range):
        hexview = psd_HexView(self.psd_project.analyzer.pe, memory_range)
        self.add_view(memory_range.get_range(), hexview)

    def add_codeview(self, memory_range):
        codeview = psd_CodeView(self.psd_project.analyzer.pe, memory_range)
        self.add_view(memory_range.get_range(), codeview)

    def add_headerview(self, memory_range):
        headerview = psd_HeaderView(self.psd_project.analyzer.pe, memory_range)
        self.add_view(memory_range.get_range(), headerview)

    def create_views(self):
        # This is the function that should be called after the PE file analysis
        # We should add here logic for creating view for each part of code
        rangemap_lst = self.psd_project.analyzer.get_address_section_rmp()
        for memory_range_rm in rangemap_lst.get_range_map_lst():
            display = memory_range_rm.get_memory_range_metadata().get_display()
            if display == "hexview":
                self.add_hexview(memory_range_rm)
            elif display == "codeview":
                self.add_codeview(memory_range_rm)
            elif display == "headerview":
                self.add_headerview(memory_range_rm)
            else:
                print "Unknown display type:", display

        #print self.addressview_rangemap_list

    def get_all_html_empty_lines(self):
        lines_range = self.addressview_rangemap_list.get_all_lines_range()
        range_length =  (lines_range[1]-lines_range[0]) + 1
        linechunks = int(math.ceil(range_length / self.linechunk_size))
        str_chunk_list = []
        for lchunk in xrange(linechunks):
            str_line_list = []
            start_line = lines_range[0] + lchunk * self.linechunk_size
            end_line = min(start_line + self.linechunk_size, lines_range[1])
            for line_idx in xrange(start_line,end_line +1):
                str_line_list.append(self.psd_html_generator.html_line_wrap(line_idx, ".") + "\n")

            chunk_html = self.psd_html_generator.html_lineschunk_wrap(lchunk, ''.join(str_line_list))
            str_chunk_list.append(chunk_html)

        return ''.join(str_chunk_list)

    def get_html_line(self, line_id):
        return self.addressview_rangemap_list.get_html_line(line_id)

    def get_html_lines(self, lines_range_tup):
        return self.addressview_rangemap_list.get_html_lines(lines_range_tup)

    def get_all_html_lines(self):
        return self.addressview_rangemap_list.get_all_html_lines()

    def get_line_id_by_address(self, address):
        # find the correct view
        view = self.addressview_rangemap_list.get_view_by_address(address)
        line_id = view.get_line_id_by_address(address)
        if line_id is not None:
            return line_id
        else:
            return -1

    ## Experimental:
    def get_linechunk(self, lineschunk_id):
        start_line = lineschunk_id*self.linechunk_size
        linesrange = (start_line, start_line + self.linechunk_size)
        html_lines_str = self.get_html_lines(linesrange)
        return self.psd_html_generator.html_lineschunk_wrap(lineschunk_id, html_lines_str)