from Model.machine import Machine
from Controller.connection import connect


def getAllMachines():
    db = connect()
    docs = db.collection('macchinario').stream()
    machines = dict()
    for doc in docs:
       machine = Machine.from_dict(doc.to_dict())
       machines[machine.name] = machine
    return machines


def updateMachineStatus(machine):
    db = connect()
    machine_ref = db.collection('macchinario').doc(machine.name)
    machine_ref.update(machine.toJSON())

def storeMachine(machine):
    db = connect()
    machine_ref = db.collection('macchinario').doc(machine.name)
    machine_ref.set(machine.toJSON())
