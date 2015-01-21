class psd_View(object):
    def __init__(self, pe, memory_range):
        self._memory_range = memory_range
        self._address_range = memory_range.get_range()
        self._memory_range_metadata = memory_range.get_memory_range_metadata()
        self._pe = pe
        self._line_range = (0, 0)

    def update_line_range(self, base_line):
        linecount = self.calculate_line_count()
        new_line_range = (base_line, base_line + linecount)
        self.set_lines(new_line_range)
        return new_line_range

    def set_lines(self, lines_tup):
        self._line_range = lines_tup

    def get_lines(self):
        return self._line_range

    def get_lines_intersection(self, other_lines_tup):
        """
        :param other_lines_tup: other tuple of lines range
        :return: The intersection if they intersect. otherwise - None
        """
        if self._line_range[0] > other_lines_tup[1] or self._line_range[1] < other_lines_tup[0]:
            return None

        start_line = max(self._line_range[0], other_lines_tup[0])
        end_line = min(self._line_range[1], other_lines_tup[1])

        return (start_line, end_line)

    def absolute_lines_to_relative(self, rel_line_tup):
        start_rel = rel_line_tup[0] - self._line_range[0]
        end_rel = start_rel + (rel_line_tup[1] - rel_line_tup[0])
        return start_rel, end_rel

    def calculate_line_count(self):
        raise NotImplementedError()

    def get_html_lines(self, line_range_tup):
        raise NotImplementedError()

    def get_line_id_by_address(self, address):
        rel_line = self.find_line_by_address(address)
        if rel_line is not None:
            return rel_line + self._line_range[0]
        else:
            return None

    def html_line_wrap(self, line_num, line_str):
        parity = "line-even" if line_num % 2 == 0 else "line-odd"
        return "<span class=\"line {0}\" id=\"{1:d}\">{2}</span>".format(parity, line_num, line_str)