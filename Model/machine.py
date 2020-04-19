from Model.oee import OEE
from Model.hour_detail import HourDetail
import copy


class Machine:
    def __init__(self):
        pass

    def addOEE(self, oee, period_id):
        self.oee[period_id] = oee

    @staticmethod
    def from_dict(source):
        obj = Machine()
        for x in source:
            if x == "oee":
                list_oee = dict()
                for y in source[x]:
                    obj_oee = OEE()
                    for z in source[x][y]:
                        if z == "hour_detail":
                            list_hour_detail = list()
                            for item_list_hour_detail in source[x][y][z]:
                                obj_hour_detail = HourDetail()
                                for prop in item_list_hour_detail:
                                    setattr(obj_hour_detail, prop, item_list_hour_detail[prop])
                                list_hour_detail.append(obj_hour_detail)
                            source[x][y][z] = list_hour_detail
                        setattr(obj_oee, z, source[x][y][z])
                    list_oee[y] = obj_oee
                setattr(obj, x, list_oee)
            else:
                setattr(obj, x, source[x])
        return obj

    def toJSON(self):
        dict = copy.deepcopy(self.__dict__)
        for x in dict['oee']:
            dict['oee'][x] = dict['oee'][x].toJSON()
        return dict
