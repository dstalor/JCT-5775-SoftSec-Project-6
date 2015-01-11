from AddressViewRangeMap import *

class psd_Visualizer:
    def __init__(self, psd_project):
        self.psd_project = psd_project
        self.addressview_rangemap_list = AddressViewRangeMapList()

    def add_view(self, addressrange, view):
        self.addressview_rangemap_list.add_range_map(AddressViewRangeMap(addressrange, view))

    def add_hexview(self,addressrange):
        hexview = HexView(self.psd_project.pe, addressrange)
        self.add_view(addressrange, hexview)

    def create_views(self):
        # This is the function that should be called after the PE file analysis
        # We should add here logic for creating view for each part of code
        hex_data_ranges = self.psd_project.get_address_range()
        self.add_hexview(hex_data_ranges)

    def get_lines(self, lines_range_tup):
        return self.addressview_rangemap_list.get_lines(lines_range_tup)

    def get_all_lines(self):
        return self.addressview_rangemap_list.get_all_lines()

    def print_disassembly(self, psd_project):
        pass

