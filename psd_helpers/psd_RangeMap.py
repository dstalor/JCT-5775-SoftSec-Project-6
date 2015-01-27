
class psd_RangeMap(object):
    """
    class which represent mapping between a range-tuple (start,end) to an object
    """
    def __init__(self,range_tup, obj):
        assert type(range_tup) is tuple, " first argument must be a range tuple (start,end))"

        self._rstart = 0
        self._rend = 0
        self.set_range(range_tup)
        self._obj = obj

    def is_range_contains_value(self, value):
        return value>=self._rstart and value <=self._rend

    def is_range_contains_range(self, range_tup):
        return self._rstart<=range_tup[0] and self._rend>=range_tup[1]

    def is_range_contained(self, range_tup):
        return self._rstart>=range_tup[0] and self._rend<=range_tup[1]

    def is_range_contains_range_exclusive(self, range_tup):
        return self.is_range_contains_range(range_tup) and not (range_tup[0]==self._rstart or range_tup[1]==self._rend)

    def is_range_contained_exclusive(self, range_tup):
        return self.is_range_contained(range_tup) and not (range_tup[0]==self._rstart or range_tup[1]==self._rend)

    def is_range_overlaps(self,range_tup):
        return self.is_range_contains_value(range_tup[0]) or self.is_range_contains_value(range_tup[1])

    def is_range_intersects(self,range_tup):
        return self.is_range_overlaps(range_tup) and self.is_range_contained(range_tup)

    def is_range_same(self, range_tup):
        return self._rstart == range_tup[0] and self._rend == range_tup[1]

    def set_range(self, range_tup):
        self._rstart = range_tup[0]
        self._rend = range_tup[1]

    def get_range(self):
        return (self._rstart, self._rend)

    def get_range_start(self):
        return self._rstart

    def get_range_end(self):
        return self._rend

    def set_obj(self, obj):
        self._obj = obj

    def get_obj(self):
        return self._obj

    #implementing less-then for sorting
    def __lt__(self, other_rangemap):
        return self._rstart < other_rangemap.get_range_start()

    def __str__(self):
        return "("+hex(self._rstart)+", "+ hex(self._rend)+") "+str(self._obj)



class RangeMapList(object):
    def __init__(self):
        self._range_map_lst = []

    def add_range_map(self, new_rangemap):
        n_range = new_rangemap.get_range()
        (n_start, n_end) = n_range

        #remove ranges that conatined in the new one
        self._range_map_lst[:] = [rm for rm in self._range_map_lst if not rm.is_range_contained(n_range)]

        for rm in self._range_map_lst:
            (rm_start, rm_end) = rm.get_range()

            if rm.is_range_contains_range(n_range):
                # rm fully contains the new range
                # we might need to dived rm into two
                if rm_start!=n_start:
                    start=rm_start
                    end=n_start-1
                    # rm can be class that inherit from RangeMap, therefore we use type(rm)(...)
                    self._range_map_lst.append(type(rm)((start, end), rm.get_obj()))
                if rm_end!=n_end:
                    start=n_end+1
                    end=rm_end
                    self._range_map_lst.append(type(rm)((start, end), rm.get_obj()))
                self._range_map_lst.remove(rm)
                # since we found a range the contains all the new one,
                # we don't need to do any more changes
                break

            if rm.is_range_contains_value(n_start):
                rm.set_range((rm_start, n_start-1))

            if rm.is_range_contains_value(n_end):
                rm.set_range((n_end+1, rm_end))



        self._range_map_lst.append(new_rangemap)
        self._range_map_lst.sort()

    def remove_range_map(self, range_tup):
        for rm in self._range_map_lst:
            if rm.is_range_same(range_tup):
                self._range_map_lst.remove(rm)
                return

    def get_range_map_lst(self):
        return self._range_map_lst

    def __str__(self):
        str=""
        for rm in self._range_map_lst:
            str+= rm.__str__()
        return str

    def get_rm_by_value(self, value):
        """
        :return: the rangemap includes value. None if no range is found.
        """
        for rm in self._range_map_lst:
            if rm.is_range_contains_value(value):
                return rm

        return None

if __name__ == "__main__":

    lrm = RangeMapList()
    def addrm(range_tup,str_obj):
        lrm.add_range_map(psd_RangeMap(range_tup, str_obj))
        print lrm


    addrm((0,1000),"base")
    addrm((0,50),"start")
    addrm((800,1000),"end")
    addrm((500,600),"middle")
    addrm((550,600),"overlap_middle_top")
    addrm((500,510),"overlap_middle_botttom")
    addrm((520,530),"overlap_middle_middle")
    addrm((400,500),"overlap_outside_bottom")
    addrm((600,700),"overlap_outside_top")
    addrm((40,700),"intersect_all_middle")