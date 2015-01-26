from psd_helpers.psd_RangeMap import *
from psd_visualizer.psd_AddressViewRangeMap import *

class psd_AddressViewRangeMapList(RangeMapList):
    def add_range_map(self, new_addressview_rangemap):
        super(psd_AddressViewRangeMapList, self).add_range_map(new_addressview_rangemap)
        self.update_line_ranges()

    def update_line_ranges(self):
        base_line = 0
        for rm in self._range_map_lst:
            base_line = rm.update_line_range(base_line)

    def get_html_line(self, line_id):
        line_str=""
        for rm in self._range_map_lst:
            view = rm.get_obj()
            line_str = view.get_html_lines((line_id, line_id))
            if line_str != "":
                break
        return line_str

    def get_html_lines(self, lines_range):
        str_lst = []
        for rm in self._range_map_lst:
            view = rm.get_obj()
            str_lst.append(view.get_html_lines(lines_range))
        return ''.join(str_lst)

    def get_all_lines_range(self):
        # we assume that the lines are sorted, so
        start = 0
        if len(self._range_map_lst) == 0:
            end = 0
        else:
            end = self._range_map_lst[-1].get_view().get_lines()[1]

        return (start, end)

    def get_all_html_lines(self):
        return self.get_html_lines(self.get_all_lines_range())

    def get_view_by_address(self, address):
        return self.get_rm_by_value(address).get_view()