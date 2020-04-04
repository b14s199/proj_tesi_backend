from influxdb import InfluxDBClient
from datetime import datetime
from datetime import timedelta


class ItemDatabase:

    def __init__(self, time_insert, traciability_code):
        self.time_insert = time_insert
        self.traciability_code = traciability_code


client = InfluxDBClient(database='newTest', host='localhost', port=8086, username='root', password='root')
rs = list((client.query(
    "SELECT * FROM prova4 WHERE time >= '2019-12-05T00:00:00Z' AND time < '2019-12-06T00:00:00Z'")).get_points())

f = open("testb.txt", "w+")
old = None
diff = timedelta(seconds=0, minutes=0, hours=0)
differences = list()

for x in rs:
    if len(x["time"]) == 22:
        # format transformation
        x["time"] = x["time"][:-3] + "Z"
    datetime_object = datetime.strptime(x["time"], '%Y-%m-%dT%H:%M:%SZ')
    new = ItemDatabase(datetime_object, x["Traciability_Code"])

    if old is None:
        old = ItemDatabase(datetime_object, x["Traciability_Code"])

    actual_difference = new.time_insert - old.time_insert
    if (actual_difference > timedelta(
            seconds=30) and new.traciability_code == old.traciability_code) or (actual_difference > timedelta(
            minutes=3) and new.traciability_code != old.traciability_code):
        differences.append((old, new))
        diff += new.time_insert - old.time_insert
    old = new

print("Pausa totale nella giornata del 2019-12-05: " + str(diff))
f.close()
for x, y in differences:
    print("Pausa dalle ", x.time_insert, " alle ", y.time_insert)


start = datetime.strptime("2019-12-05T00:00:00Z", '%Y-%m-%dT%H:%M:%SZ')
end = datetime.strptime("2019-12-06T00:00:00Z", '%Y-%m-%dT%H:%M:%SZ')
while start <= end:
    new = start + timedelta(hours=1)
    count = timedelta(hours=0, minutes=0, seconds=0)
    for x, y in differences:
        if x.time_insert.hour == start.hour:
            if y.time_insert.hour != start.hour:
                count += new - x.time_insert
                x.time_insert = new
            else:
                count += y.time_insert - x.time_insert
    #print("Dalle " + str(start) + " alle " + str(new) + " ci sono stati :" + str(count))
    start += timedelta(hours=1)