import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

def connect():
    pathMac = "/Users/biagioboi/Desktop/tesi/proj_tesi_backend/Config/privateKeyFirestore.json"
    pathWin = "D:\\xampp\\htdocs\\proj_tesi_backend\\"
    cred = credentials.Certificate(pathMac)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db

def old():
    pathMac = "/Users/biagioboi/Desktop/tesi/proj_tesi_backend/"
    pathWin = "D:\\xampp\\htdocs\\proj_tesi_backend\\"

    dfs = pd.read_excel(pathMac + "Config/machines_config.xlsx")
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

    fp = open(pathMac + "Output/machines_config.txt", mode='w+')
    print(to_print, file=fp)
