from psd_View import psd_View
import time
import exceptions

class psd_HeaderView(psd_View):
    def __init__(self, pe, memory_range):
        super(psd_HeaderView, self).__init__(pe, memory_range)
        self.header = self._memory_range.get_memory_range_metadata().get_header()
        self.html_lines = []
        self.create_html_lines()

    def calculate_line_count(self):
        title_lines = 2
        end_lines = 1
        return len(self.header.__keys__) + title_lines + end_lines

    def create_html_lines(self):
        self.html_lines = []

        html_title_str = self.html_header_title(self.header.name, self._memory_range.get_range())
        self.html_lines.append('\n'+html_title_str+'\n')

        for keys in self.header.__keys__:
            for key in keys:
                str_field_name = self.field_name_html(key)
                str_rowheader = self.html_rowheader(self.header.__field_offsets__[key] + self.header.__file_offset__)
                str_more_info = ""
                str_field_value = ""

                val = getattr(self.header, key)
                if isinstance(val, int) or isinstance(val, long):
                    val_str = '0x%-8X' % (val)

                    more_info = None
                    jump_location = None

                    if key == 'TimeDateStamp' or key == 'dwTimeStamp':
                        try:
                            more_info = ' [%s UTC]' % time.asctime(time.gmtime(val))
                        except exceptions.ValueError, e:
                            more_info = ' [INVALID TIME]'
                    elif key in ['VirtualAddress']:
                        jump_location = val_str

                    str_constant = self.constant_html(val, jump_location)
                    str_field_value = self.field_value_html(str_constant)
                    if more_info:
                        str_more_info = self.more_info_html(more_info)
                else:
                    val_str = ''.join(filter(lambda c:c != '\0', str(val)))
                    str_field_value = self.field_value_html(val_str)

                self.html_lines.append(str_rowheader + str_field_name + str_field_value + str_more_info+ "\n")
        self.html_lines.append("\n")

    def get_html_line_list(self, line_range_tup):
        return self.html_lines[line_range_tup[0]: line_range_tup[1]+1]

    def html_header_title(self, header_name, address_tup):
        return "<span class=\"headerview-title\">***   {0}   [0x{1:08x} -> 0x{2:08x}]</span></span>".format(header_name, *address_tup)

    def html_rowheader(self, address):
        return ("<span class=\"headerview-row-header\">"+" "*20+" <span class=\"header-address\">0x{0:08x}</span>: </span>").format(address)

    def constant_html(self, constant_str, c_jump_address=None):
        class_str = "constant"
        jump_str = ""
        if c_jump_address is not None:
            class_str += " jump"
            jump_str = " data-jump-location=\""+c_jump_address+"\""
        #print ("<span class=\"{0}\""+jump_str+">{1}</span>").format(class_str, constant_str)
        return ("<span class=\"{0}\""+jump_str+">{1}</span>").format(class_str, constant_str)

    def field_name_html(self, field_name):
        return ("<span class=\"headerview-field-name\"> {0: <30} </span>").format(field_name+":")

    def more_info_html(self, info_str):
        return ("<span class=\"headerview-more-info\"> {0} </span>").format(info_str)

    def field_value_html(self, value_str):
        return ("<span class=\"headerview-field-value\"> {0} </span>").format(value_str)