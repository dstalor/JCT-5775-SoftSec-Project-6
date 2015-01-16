import math


class View(object):
    def __init__(self, pe, memory_range):
        self._memory_range = memory_range
        self._address_range = memory_range.get_range()
        self._memory_range_metadata = memory_range.get_memory_range_metadata()
        self._pe = pe
        self._line_range=(0,0)

    def calculate_line_count(self):
        raise NotImplementedError()

    def update_line_range(self, base_line):
        linecount = self.calculate_line_count()
        new_line_range = (base_line, base_line + linecount)
        self.set_lines(new_line_range)
        return new_line_range

    def get_html_lines(self, line_range_tup):
        raise NotImplementedError()

    def set_lines(self, lines_tup):
        self._line_range = lines_tup

    def get_lines(self):
        return self._line_range

    def get_lines_intersection(self, other_lines_tup):
        """
        :param other_lines_tup: other tuple of lines range
        :return: The intersection if they intersect. otheriwse - None
        """
        if self._line_range[0] > other_lines_tup[1] or self._line_range[1] < other_lines_tup[0]:
            return None

        start_line = max(self._line_range[0] ,other_lines_tup[0])
        end_line = min(self._line_range[1], other_lines_tup[1])

        return (start_line, end_line)

    def absolute_lines_to_relative(self, rel_line_tup):
        start_rel = rel_line_tup[0]-self._line_range[0]
        end_rel = start_rel + (rel_line_tup[1] - rel_line_tup[0])
        return start_rel, end_rel

class HexView(View):
    def __init__(self, pe, memory_range, offset=0x10):
        super(HexView, self).__init__(pe, memory_range)
        self._offset = offset

    def calculate_line_count(self):
        return self.find_line_by_address(self._address_range[1])

    # def get_lines_str(self, line_range_tup):
    #     line_start = line_range_tup[0] if line_range_tup[0] >
    #
    #     address_start = self.find_address_by_line(line_start)
    #     fmt = "".join(['{' + str(i) + ':02x} ' for i in range(self._offset)])
    #     str_out = ""
    #     img = self._pe.get_memory_mapped_image()
    #     # "{0:02x}".format(ord(img[0]))
    #
    #     for l in range(line_start, line_end + 1):
    #         bytes = map(ord, img[address_start:address_start + self._offset])
    #         str_out += fmt.format(*bytes) + "\n"
    #         address_start += self._offset
    #
    #     print str_out
    #     return str_out

    def get_html_lines(self, line_range_tup):
        intersect_lines = self.get_lines_intersection(line_range_tup)
        if not intersect_lines:
            return ""

        (line_start, line_end) = self.absolute_lines_to_relative(intersect_lines)
        address_start = self.find_address_by_line(line_start)
        str_out = ""
        img = self._pe.get_memory_mapped_image()

        for l in range(line_start, line_end + 1):
            bytes = map(ord, img[address_start:address_start + self._offset])
            str_out += self.html_line(address_start, bytes)
            address_start += self._offset

        #print str_out
        return str_out

    def html_line(self, start_address, bytes):
        str_rowheader = self.html_rowheader(self._memory_range_metadata.get_range_name() , start_address)
        str_bytedata = ""
        str_asciidata = ""
        for i in range(len(bytes)):
            byte = bytes[i]
            if (i + 1) % 4 == 0:
                specialclass = "spaceafter"
            elif i == len(bytes) - 1:
                specialclass = "final"
            else:
                specialclass = ""

            str_bytedata += self.html_bytedata(start_address + i, byte, specialclass)
            str_asciidata += self.html_byte_ascii(start_address + i, byte)

        return str_rowheader + str_bytedata + str_asciidata + "\n"

    def html_rowheader(self, rangename, address):
        return "<span class=\"datahex-row-header\">{0: >10} 0x{1:08x}: </span>".format(rangename, address)

    def html_bytedata(self, address, byte, specialclass=""):
        return "<span id=\"datahex-{0:08x}-data\" class=\"datahex-byte-data {1:s}\">{2:02x}</span>".format(address, specialclass, byte)

    def html_byte_ascii(self, address, byte, specialclass=""):
        return "<span id=\"datahex-{0:08x}-ascii\" class=\"datahex-byte-ascii {1:s}\">{2:s}</span>".format(address, specialclass,
                                                                                           self.get_visible_ascii(
                                                                                               chr(byte)))

    # <span id="00000-ascii" class="byte-ascii">&#77;</span>
    # def html_bytedata2(self, address, byte, spaceafter=False):
    #     return self.html_node("span",{"id":"{0:08x}-data".format(address), "class": "byte-data{ 1:s}".format()})
    #
    # def html_node(self, tag_str, att_dic, text):
    #     att_str = "".join([att+"="+att_dic[att]+" " for att in att_dic])
    #     return "<"+tag_str+" "+att_str+">"+text+"</"+tag_str+">"

    def find_line_by_address(self, address):
        bytes = (address - self._address_range[0])
        return int(math.floor(bytes / self._offset))

    def find_address_by_line(self, line):
        return (line * self._offset) + self._address_range[0]

    def get_visible_ascii(self, char):
        # TODO: 1. creating this list each time is no efficient.
        # TODO: 2. also, should be moved to helper-functions
        control_chars = ''.join(map(chr, range(0, 32) + range(127, 160)))
        if char in control_chars or ord(char) >= 128:
            return '.'
        else:
            return char


if __name__ == "__main__":
    HexView("da", (9, 100))