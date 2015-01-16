from ThirdParty.pefile.pefile import PE
from psd_MemoryRangeMetadata import psd_MemoryRangeMetadata
from psd_MemoryRangeRangeMap import psd_MemoryRangeRangeMap
from psd_helpers.RangeMap import RangeMapList

class psd_Analyzer(object):
    def __init__(self, psd_project):
        self.psd_project = psd_project
        self.address_section_rmp = RangeMapList()
        self.pe = None

    def load_executable(self, filename):
        """
        This functions calls pefile lib in order to load executable and analyze it header.
        the result will be in  self.pe instance.
        It must be called before any other analyziss takes place!
        :param filename: executable file name
        :return: None
        """
        self.pe = PE(filename)

        self.analyze_pe()

    def analyze_pe(self):
        """
        This function calls all the analyze functions after the self.pe created by load_executable
        :return: Nona
        """

        #self.analyze_header() #This function  calls pefile and the result will be in self.pe
        self.analyze_memorymap()
        #self.disassemble()    #This function calls capstone and the result will be in ?

    def analyze_memorymap(self):
        """
        This function fills self.address_section_rmp(rangemap list),
        which is basically a mapping between memory addresses and sections_data
        :return: None
        """
        # setting all range as 'unknown' as we start
        base_range = psd_MemoryRangeRangeMap(self.get_address_range(), psd_MemoryRangeMetadata("unknown"))
        self.address_section_rmp.add_range_map(base_range)

        # add sections
        for section in self.pe.sections:
            address_range = (section.VirtualAddress, section.VirtualAddress + section.Misc_VirtualSize)

            #TODO: the [:5] is a workaround to strip the non-printable bytes.
            # do real striping

            new_range = psd_MemoryRangeRangeMap(address_range, psd_MemoryRangeMetadata(section.Name[:4], section))
            self.address_section_rmp.add_range_map(new_range)
        print self.address_section_rmp



    def get_address_range(self):
        """
        :return: Address range of all memory mapped image
        """
        end = len(self.pe.get_memory_mapped_image()) - 1
        return (0, end)

    def get_pe(self):
        return self.pe

    def get_address_section_rmp(self):
        return self.address_section_rmp