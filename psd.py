from psd_Project import *
from psd_GUI.psd_GUI import psd_GUI


class psd:
    def __init__(self):
        self.psd_project = None

    def create_new_project(self, filename=None):
        self.psd_project = psd_Project(self, filename)


def test_HexView(psd_project):
    from psd_visualizer.psd_HexView import psd_HexView

    hv = psd_HexView(psd_project.pe, (0, 3000))
    hv.get_html_lines((0, 50))


if __name__ == "__main__":
    psd_main = psd()
    psd_main.create_new_project()

    # psd_main.psd_project.pe.print_info()

    # tests
    # test_HexView(psd_main.psd_project)

    psd_GUI = psd_GUI(psd_main)
    #filename = psd_GUI.get_filename()
    psd_GUI.run()

