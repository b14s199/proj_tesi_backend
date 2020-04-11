from Controller import machineController
from Controller.connection import influxDB
from datetime import datetime
from datetime import timedelta
import time

# for simulating purpose we define actual time, in future this date it's now date
date = datetime(year=2019, month=12, day=5, hour=20, minute=30, second=0, microsecond=0)

machines = machineController.getAllMachines()
prev_time = date.replace(hour=0, minute=0, second=0, microsecond=0)  # to obtain the first daily date

while True:
    dateLimit = date.replace(minute=0, second=0, microsecond=0)  # to obtain actual date (just hour), where we have to stop
    while prev_time < dateLimit:  # used to sync the older period, from midnight to actual hour
        new_time = prev_time + timedelta(
            hours=1)  # to increase time hour by hour and then analyze the data(s) between the two hours
        influx = influxDB()  # get influxDB connection
        for machine in machines:  # foreach machine in db update oee period with newer data
            rs = influx.query(
                "SELECT * FROM prova4 WHERE time >= '" + prev_time.strftime("%Y-%m-%dT%H:%M:%SZ") + "' AND "
                + "time < '" + new_time.strftime("%Y-%m-%dT%H:%M:%SZ") + "' AND "
                + "Program = '" + machine.name + "'")  # get all machine data in considered period
            for data in rs:
                #  TODO: define the operation to compute oee on stored data between defined period
                pass
        prev_time = new_time
    next_hour = (date + timedelta(hours=1)).replace(minute=0, second=0)  # to know which is the next hour
    second_to_wait = (next_hour - date).total_seconds()  # to know how many seconds we have to wait for the next period
    time.sleep(second_to_wait)  # sleep for waiting period
    date = datetime.now()  # set new time


