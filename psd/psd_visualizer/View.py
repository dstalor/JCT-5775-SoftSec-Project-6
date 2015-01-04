import pefile.pefile
import math

class View(object):
    def __init__(self, pe, address_range):
        self._address_range = address_range
        self._pe = pe

    def calculate_line_count(self):
        raise NotImplementedError()

    def calculate_line_range(self, base_line):
        linecount = self.calculate_line_count()
        return (base_line, base_line+linecount)

    def get_lines(self, line_range_tup):
        raise NotImplementedError()

class HexView(View):
    def __init__(self, pe, address_range, offset=0x10):
        super(HexView, self).__init__(pe, address_range)
        self._offset = offset

    def calculate_line_count(self):
        return self.find_line_by_address(self.address_range[1])

    def get_lines(self, line_range_tup):
        (line_start, line_end) = line_range_tup
        address_start = self.find_address_by_line(line_start)
        for l in range(line_start, line_end+1):
            


    def find_line_by_address(self, address):
        bytes = (address-self._address_range[0])+1
        return int(math.ceil(bytes/self._offset))

    def find_address_by_line(self, line):
        return (line * self._offset) + self._address_range[0]



if __name__ == "__main__":
    HexView("da",(9,100))




