from datetime import datetime


def clean_data_frames(df):
    first_row = df.loc[0]  # prendo la prima riga
    date = first_row[1:4]  # prendo la data
    time = first_row[4:7]  # prendo l'ora
    dateString = '/'.join(date)
    timeString = ':'.join(time)
    completeDate = dateString + " " + timeString
    datetime_object = datetime.strptime(completeDate, '%y/%m/%d %H:%M:%S')
    initialTs = datetime_object.timestamp()  # timestamp initial
    dfMod = df.iloc[:, :-3]  # tolgo le ultime 3 colonne che non sono in realta valide
    dfMod = dfMod.loc[0:]
    dfMod = dfMod.tail(-2)  # cancello le righe che rappresentan il time e i ms nel csv
    dfMod = dfMod.reset_index(drop=True)  # resetto il count delle righe
    dfMod.columns = dfMod.iloc[0]  # trasformo la prima riga nell'handler
    dfMod = dfMod[1:]
    lenDfMod = len(dfMod)
    generateTimestamp = [int(initialTs + i * 100) for i in range(0, lenDfMod)]
    print(generateTimestamp)
    dfMod['Timestamp'] = generateTimestamp
    # dfMod.to_csv("/home/broke31/Desktop/PICO/test3.csv", sep=',', encoding='utf-8', header=True, index=False)
    return dfMod

def clean_data_frame(df):
    dfMod = df
    dfMod.columns = dfMod.iloc[0]  # trasformo la prima riga nell'handler
    dfMod = dfMod[1:]
    # dfMod.to_csv("/home/broke31/Desktop/PICO/test3.csv", sep=',', encoding='utf-8', header=True, index=False)
    return dfMod
