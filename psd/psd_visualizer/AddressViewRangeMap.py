from psd_helpers.RangeMap import *
from View import *

class AddressViewRangeMap(RangeMap):
    def __init__(self, address_range_tup, view_obj):
        assert isinstance(view_obj, View), "second argument must an object of type View!"
        super(AddressViewRangeMap, self).__init__(address_range_tup, view_obj)

    def update_line_range(self, base_line):
        new_line_range = self._obj.update_line_range(base_line)
        # return the new base line: the next line after this line-range
        return new_line_range[1]+1

    def get_view(self):
        return self._obj

class AddressViewRangeMapList(RangeMapList):
    def add_range_map(self,new_addressview_rangemap):
        super(AddressViewRangeMapList, self).add_range_map(new_addressview_rangemap)
        self.update_line_ranges()

    def update_line_ranges(self):
        base_line = 0
        for rm in self._range_map_lst:
            base_line = rm.update_line_range(base_line)

    def get_html_lines(self, lines_range):
        str = ""
        for rm in self._range_map_lst:
            view = rm.get_obj()
            str += view.get_html_lines(lines_range)
        return str

    def get_all_lines_range(self):
        #we assume that the lines are sorted, so
        start = 0
        if not self._range_map_lst[-1]:
            end = 0
        else:
            end = self._range_map_lst[-1].get_view().get_lines()[1]

        return (start, end)

    def get_all_html_lines(self):
        return self.get_html_lines(self.get_all_lines_range())