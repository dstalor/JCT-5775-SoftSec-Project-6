from psd_helpers.psd_RangeMap import *
from psd_View import *


class psd_AddressViewRangeMap(psd_RangeMap):
    def __init__(self, address_range_tup, view_obj):
        assert isinstance(view_obj, psd_View), "second argument must be an object of type View!"
        super(psd_AddressViewRangeMap, self).__init__(address_range_tup, view_obj)

    def update_line_range(self, base_line):
        new_line_range = self._obj.update_line_range(base_line)
        # return the new base line: the next line after this line-range
        return new_line_range[1] + 1

    def get_view(self):
        return self._obj
