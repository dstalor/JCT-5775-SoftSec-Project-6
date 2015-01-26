#TODO: move all html creation logic to here &
#TODO: make this abstrct class and inherit to full/light html generators

class psd_HTMLGenerator(object):
    def html_line_wrap(self, line_num, line_str):
        parity = "line-even" if line_num % 2 == 0 else "line-odd"
        return "<span class=\"line {0}\" id=\"{1:d}\">{2}</span>\n".format(parity, line_num, line_str)
