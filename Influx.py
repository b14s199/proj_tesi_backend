from influxdb import DataFrameClient
import pandas as pd


def write_into_influx(host='localhost', port=8086, dfMod=None):
    user = 'root'
    password = 'root'
    dbname = 'newTest'
    protocol = 'line'
    client = DataFrameClient(host, port, user, password, dbname)
    dbs = client.get_list_database()
    if dbname not in dbs:
        client.create_database(dbname)
    dfMod = dfMod.set_index(['Timestamp'])
    dfMod.index = pd.to_datetime(dfMod.index, unit='ms')
    dfMod[['Weld speed']] = dfMod[['Weld speed']].apply(pd.to_numeric)
    dfMod[['Command current']] = dfMod[['Command current']].apply(pd.to_numeric)
    dfMod[['Current output']] = dfMod[['Current output']].apply(pd.to_numeric)
    dfMod[['Command voltage']] = dfMod[['Command voltage']].apply(pd.to_numeric)
    dfMod[['Voltage output']] = dfMod[['Voltage output']].apply(pd.to_numeric)
    dfMod[['Short count']] = dfMod[['Short count']].apply(pd.to_numeric)
    dfMod[['Pulse frequency']] = dfMod[['Pulse frequency']].apply(pd.to_numeric)
    dfMod[['Motor current']] = dfMod[['Motor current']].apply(pd.to_numeric)
    dfMod[['Wire speed']] = dfMod[['Wire speed']].apply(pd.to_numeric)
    dfMod[['Instant arc-lack time']] = dfMod[['Instant arc-lack time']].apply(pd.to_numeric)
    client.write_points(dfMod, 'prova4', protocol=protocol)
