from Model.oee import OEE
import copy


class Machine:
    def __init__(self):
        pass

    def addOEE(self, oee, period_id):
        self.oee.update(period_id, oee)

    @staticmethod
    def from_dict(source):
        obj = Machine()
        for x in source:
            if x == "oee":
                list_oee = dict()
                for y in source[x]:
                    obj_oee = OEE()
                    for z in source[x][y]:
                        setattr(obj_oee, z, source[x][y][z])
                    list_oee[y] = obj_oee
                setattr(obj, x, list_oee)
            else:
                setattr(obj, x, source[x])
        return obj

    def toJSON(self):
        dict = copy.deepcopy(self.__dict__)
        for x in dict['oee']:
            dict['oee'][x] = dict['oee'][x].__dict__
        return dict
