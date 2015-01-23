from ThirdParty.pefile.pefile import PE
from capstone import *

from psd_helpers.psd_Helpers import *
from psd_MemoryRangeMetadata import psd_MemoryRangeMetadata
from psd_MemoryRangeRangeMap import psd_MemoryRangeRangeMap
from psd_helpers.psd_RangeMap import RangeMapList

class psd_Analyzer(object):
    def __init__(self, psd_project):
        self.psd_project = psd_project
        self.address_section_rmp = RangeMapList()
        self.pe = None

        #TODO: Architecture and mode is currently hardcoded - add auto recognition
        self.asm_architecture = CS_ARCH_X86
        self.asm_mode = CS_MODE_32
        self.disassembler = Cs(self.asm_architecture, self.asm_mode)
        self.disassembler.detail = True

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

        #
        self.pe.print_info()

    def analyze_pe(self):
        """
        This function calls all the analyze functions after the self.pe created by load_executable
        :return: Nona
        """

        #self.analyze_header() #This function  calls pefile and the result will be in self.pe
        self.analyze_memorymap()
        self.disassemble()    #This function calls capstone and the result will be in ?

    def analyze_memorymap(self):
        """
        This function fills self.address_section_rmp(rangemap list),
        which is basically a mapping between memory addresses and sections_data
        :return: None
        """
        # setting all range as 'unknown' as we start
        base_range = psd_MemoryRangeRangeMap(self.get_address_range(), psd_MemoryRangeMetadata("unmapped"))
        self.address_section_rmp.add_range_map(base_range)

        # add headers
        headers = { self.pe.DOS_HEADER : "DOS_HEADER",
                    self.pe.NT_HEADERS : "NT_HEADERS",
                    self.pe.FILE_HEADER: "FILE_HEADER"}

        if hasattr(self.pe, "OPTIONAL_HEADER"):
            headers[self.pe.OPTIONAL_HEADER] = "OPTIONAL_HEADER"

        if hasattr(self.pe, "RICH_HEADER"):
            headers[self.pe.RICH_HEADER] = "RICH_HEADER"

        if hasattr(self.pe, "VS_FIXEDFILEINFO"):
            headers[self.pe.VS_FIXEDFILEINFO] = "VS_FIXEDFILEINFO"

        if hasattr(self.pe, "VS_VERSIONINFO"):
            headers[self.pe.VS_VERSIONINFO] = "VS_VERSIONINFO"

        #adding section headers
        for s in self.pe.sections:
            headers[s] = s.Name

        #adding directories headers
        if (hasattr(self.pe, 'OPTIONAL_HEADER') and
            hasattr(self.pe.OPTIONAL_HEADER, 'DATA_DIRECTORY') ):
            for idx in xrange(len(self.pe.OPTIONAL_HEADER.DATA_DIRECTORY)):
                dir = self.pe.OPTIONAL_HEADER.DATA_DIRECTORY[idx]
                headers[dir] = dir.name

        for header, header_name in headers.iteritems():
            if header:
                phy_start_address = header.get_file_offset()
                phy_end_address = phy_start_address + header.sizeof()
                start_address = self.pe.get_physical_by_rva(phy_start_address)
                end_address= self.pe.get_physical_by_rva(phy_end_address)

                new_range = psd_MemoryRangeRangeMap((start_address, end_address), psd_MemoryRangeMetadata(header_name, display = "headerview", header = header))
                self.address_section_rmp.add_range_map(new_range)

        # add sections
        for section in self.pe.sections:
            address_range = (section.VirtualAddress, section.VirtualAddress + section.Misc_VirtualSize)

            # strip non-printable bytes from section NAME
            sec_name = strip_non_printable(section.Name)

            new_range = psd_MemoryRangeRangeMap(address_range, psd_MemoryRangeMetadata(sec_name, section))

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

    def disassemble(self):
        """
        disassemble code parts of the pe file
        :return:
        """
        #TODO: make this more efficiant and easy to use, iterating an entire list to find a specific section is ugly
        #disassemble .text section
        for rm in self.address_section_rmp.get_range_map_lst():
            sec_name = rm.get_memory_range_metadata().get_range_name()
            if sec_name == ".text":
                self.disassemble_memory_range(rm)
                break

    def disassemble_memory_range(self, memoryrange_rm):
        """
        Analyze a memory range as a code
        :param memoryrange_rm: MemoryRangeRangeMap
        :return: none
        """
        metadata = memoryrange_rm.get_memory_range_metadata()
        metadata.set_is_code(True)
        metadata.set_display("codeview")

        start, end = memoryrange_rm.get_range()
        code_bytes = self.pe.get_memory_mapped_image()[start: end+1]

        metadata.set_code_lines(self.disassemble_bytes(start, code_bytes))

    def disassemble_bytes(self, start_address, code_bytes):
        return [line for line in self.disassembler.disasm(code_bytes, start_address)]
