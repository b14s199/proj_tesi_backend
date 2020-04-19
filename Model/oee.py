import copy
from Model.hour_detail import HourDetail


class OEE:
    def __init__(self, good_pieces=None, bad_pieces=None, hour_detail=None):
        self.good_pieces = good_pieces
        self.bad_pieces = bad_pieces
        self.hour_detail = hour_detail

    def toJSON(self):
        diction = copy.deepcopy(self.__dict__)
        for x in diction:
            if isinstance(diction[x], list):
                list_hour_detail = list()
                for y in diction[x]:
                    list_hour_detail.append(y.toJSON())
                diction[x] = list_hour_detail
        return diction
