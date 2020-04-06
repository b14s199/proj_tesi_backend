import pandas as pd
from Model.machine import Machine
from Model.oee import OEE

pathMac = "/Users/biagioboi/Desktop/tesi/proj_tesi_backend/"
pathWin = "D:\\xampp\\htdocs\\proj_tesi_backend\\"

dfs = pd.read_excel(pathWin + "Config\\machines_config.xlsx")
list_machine = list()
for (name, time_production_item) in zip(dfs['nome'], dfs['tempo_produzione_pezzo']):
    machine_oee = OEE(75.8, 85, 80, 75)
    machine = Machine(name, "Run", None, None, None, None, None, None, None, time_production_item, None, None, None,
                      machine_oee)
    list_machine.append(machine)

to_print = "["
for x in list_machine:
    to_print += x.toJSON() + ","
to_print = to_print[:-1]
to_print += "]"

fp = open(pathWin + "Output\\machines_config.txt", mode='w+')
print(to_print, file=fp)
