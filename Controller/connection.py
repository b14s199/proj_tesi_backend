import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from influxdb import InfluxDBClient


def connect():
    pathMac = "/Users/biagioboi/Desktop/tesi/proj_tesi_backend/Config/privateKeyFirestore.json"
    pathWin = "D:\\xampp\\htdocs\\proj_tesi_backend\\"
    cred = credentials.Certificate(pathMac)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db


def influxDB():
    return InfluxDBClient(database='newTest', host='localhost', port=8086, username='root', password='root')
