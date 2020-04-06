import json


class Machine:
    def __init__(self, name, status, powerOn, start, beatingSpeedPerHours, startMouldAssembly, endMouldAssembly, changeOfWorkingShift, secondChangeOfWorkingShift, numExpectedProduct, numProduct, numGoodProduct, numBadProduct, oee):
        self.name = name
        self.status = status
        self.powerOn = powerOn
        self.start = start
        self.beatingSpeedPerHours = beatingSpeedPerHours
        self.startMouldAssembly = startMouldAssembly
        self.endMouldAssembly = endMouldAssembly
        self.changeOfWorkingShift = changeOfWorkingShift
        self.secondChangeOfWorkingShift = secondChangeOfWorkingShift
        self.numExpectedProduct = numExpectedProduct
        self.numProduct = numProduct
        self.numGoodProduct = numGoodProduct
        self.numBadProduct = numBadProduct
        self.oee = oee

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=2)
