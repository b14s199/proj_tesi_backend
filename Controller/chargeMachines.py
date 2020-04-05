import pandas as pd
from Model.machine import Machine

dfs = pd.read_excel("/Users/biagioboi/Desktop/tesi/proj_tesi_backend/Config/machines_config.xlsx")
list_machine = list()
for (name, time_production_item) in zip(dfs['nome'], dfs['tempo_produzione_pezzo']):
    machine = Machine(name, None, None, None, None, None, None, None, None, time_production_item, None, None, None)
    list_machine.append(machine)

to_print = "["
for x in list_machine:
    to_print += x.toJSON() + ","
to_print = to_print[:-1]
to_print += "]"

fp = open("/Users/biagioboi/Desktop/tesi/proj_tesi_backend/Output/machines_config.txt", mode='w+')
print(to_print, file=fp)
