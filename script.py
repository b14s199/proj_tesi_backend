import pandas as pd
from ClearDataframe import clean_data_frame
from Influx import write_into_influx
import os
import glob
import logging
import sys


# 1    19
# 2    10
# 3    17
# 4    16
# 5    44
# 6    24


def get_file_names(path, extension='csv'):
    os.chdir(path)
    result = glob.glob('*.{}'.format(extension))
    return result


def newFun(df):
    dfMod = df
    dfMod.columns = dfMod.iloc[0]  # trasformo la prima riga nell'handler
    dfMod = dfMod[1:]
    x = 0
    lenDfMod = len(dfMod)
    dfMod['Timestamp'][1] = int(dfMod['Timestamp'][1]) * 1000
    generateTimestamp = [int(dfMod['Timestamp'][1] + i * 100) for i in range(0, lenDfMod)]
    dfMod['Timestamp'] = generateTimestamp
    print(dfMod['Timestamp'])
    # dfMod.to_csv("/home/broke31/Desktop/PICO/test3.csv", sep=',', encoding='utf-8', header=True, index=False)
    return dfMod

def error_to_call():
    print("run the script with this parameters:")
    print("hostName: localhost")
    print("port: 8086")
    print("pathDirectory:The directory where the csv files are located")
    print("pathLog: The directory where you want to save the log file")
    exit(0)


def main(argv):
    if len(sys.argv) != 1:
        error_to_call()
    else:
        host ="localhost"
        port = 8086
        port = int(port)
        path = "/Users/biagioboi/Desktop/Pico-ProFirstSupply-master/FilePuliti8000v2.0/filePuliti8000SenzaErrore"
        pathLog = "pathLog"
        path = path
        logging.basicConfig(filename=pathLog,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)
        logging.info('path base: %s', path)
        namesFile = get_file_names(path=path)
        for name in namesFile:
            logging.info("_______________________________________")
            logging.info("analyze: %s", name)
            df = pd.read_csv(r'' + path + "/" + name, header=None)
            logging.info('Initial csv: - {}'.format(df.head()))
            logging.info("_______________________________________")
            logging.info("__________CSV AFTER CLEAN____________")
            logging.info(df)
            logging.info("__________END CLEAN____________")
            logging.info("write csv into db... host %s: port: %d", host, port)
            #dfMod = newFun(df)
            #dfMod.to_csv(path + "/" + name, sep=',', encoding='utf-8', header=True, index=False)
            dfMod = clean_data_frame(df)
            write_into_influx(host, port, dfMod)
            logging.info("__________END Write____________")


if __name__ == "__main__":
    main(sys.argv[1:])
