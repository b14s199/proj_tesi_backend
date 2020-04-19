from datetime import datetime
import copy


class HourDetail:

    def __init__(self, status=None, startHour=None, endHour=None):
        self.status = status
        self.startHour = startHour
        self.endHour = endHour

    def toJSON(self):
        diction = copy.deepcopy(self.__dict__)
        for x in diction:
            if isinstance(diction[x], datetime):
                diction[x] = diction[x].strftime("%H:%M:%S")
        return diction
