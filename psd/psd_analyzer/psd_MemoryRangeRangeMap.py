from psd_helpers.RangeMap import RangeMap
from psd_MemoryRangeMetadata import psd_MemoryRangeMetadata

class psd_MemoryRangeRangeMap(RangeMap):
    """
    This class represent a mapping between address-range and its metadata
    """

    def __init__(self, address_range_tup, memory_range_metadata):
        assert isinstance(memory_range_metadata, psd_MemoryRangeMetadata), " second argument must be a psd_MemoryRangeMetadata"
        super(psd_MemoryRangeRangeMap, self).__init__(address_range_tup, memory_range_metadata)

    def get_memory_range_metadata(self):
        return self._obj

