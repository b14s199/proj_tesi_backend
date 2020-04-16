import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from influxdb import InfluxDBClient

firestore_connection = None


def connect():
    global firestore_connection
    pathMac = "/Users/biagioboi/Desktop/tesi/proj_tesi_backend/Config/privateKeyFirestore.json"
    pathWin = "D:\\xampp\\htdocs\\proj_tesi_backend\\Config\\privateKeyFirestore.json"
    if firestore_connection is None:
        cred = credentials.Certificate(pathWin)
        firebase_admin.initialize_app(cred)
        firestore_connection = firestore.client()
    return firestore_connection


def influxDB():
    return InfluxDBClient(database='newTest', host='localhost', port=8086, username='root', password='root')
