from AddressViewRangeMap import *
from psd_visualizer.psd_HexView import psd_HexView
from psd_visualizer.psd_CodeView import psd_CodeView


class psd_Visualizer:
    def __init__(self, psd_project):
        self.psd_project = psd_project
        self.addressview_rangemap_list = AddressViewRangeMapList()

    def add_view(self, addressrange, view):
        self.addressview_rangemap_list.add_range_map(AddressViewRangeMap(addressrange, view))

    def add_hexview(self, memory_range):
        hexview = psd_HexView(self.psd_project.analyzer.pe, memory_range)
        self.add_view(memory_range.get_range(), hexview)

    def add_codeview(self, memory_range):
        codeview = psd_CodeView(self.psd_project.analyzer.pe, memory_range)
        self.add_view(memory_range.get_range(), codeview)

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
            else:
                print "Unknown display type:", display

        print self.addressview_rangemap_list

    # def get_lines(self, lines_range_tup):
    # return self.addressview_rangemap_list.get_lines(lines_range_tup)
    #
    def get_all_html_lines(self):
        return self.addressview_rangemap_list.get_all_html_lines()

    def print_disassembly(self, psd_project):
        pass

