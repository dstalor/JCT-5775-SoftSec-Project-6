__author__ = 'Noam'

class psd_MemoryRangeMetadata(object):
    """
    This class is encapsulation of meta-data about the different memory ranges.
    """
    def __init__(self, range_name = "", section = None , display = "hexview"):
        self._range_name=range_name
        #self.section_name=section_name
        self._section=section
        self._display=display

    def __str__(self):
        return "range_name:%s" %(self._range_name)

    def get_display(self):
        return self._display

    def set_display(self, display):
        self._display = display

    def get_section(self):
        return self._section

    def set_section(self, section):
        self._section = section

    def get_range_name(self):
        return self._range_name

    def set_range_name(self, str):
        self._range_name = str

