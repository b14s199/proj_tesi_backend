from Controller import machineController
from Controller.connection import influxDB
from datetime import datetime
from datetime import timedelta
from Model.machine import Machine
import time
import json

# for simulating purpose we define actual time, in future this date it's now date
date = datetime(year=2019, month=12, day=5, hour=20, minute=30, second=0, microsecond=0)

machines = machineController.getAllMachines()
prev_time = date.replace(hour=0, minute=0, second=0, microsecond=0)  # to obtain the first daily date

while True:
    dateLimit = date.replace(minute=0, second=0, microsecond=0)  # to obtain actual date (just hour), where we have to stop
    while prev_time <= dateLimit:  # used to sync the older period, from midnight to actual hour
        new_time = prev_time + timedelta(hours=1)  # to increase time hour by hour and then analyze the data(s) between the two hours
        influx = influxDB()  # get influxDB connection
        for machine in machines:  # foreach machine in db update oee period with newer data
            machine = machines[machine]
            rs = list(influx.query(
                "SELECT * FROM prova4 WHERE time >= '" + prev_time.strftime("%Y-%m-%dT%H:%M:%SZ") + "' AND "
                + "time < '" + new_time.strftime("%Y-%m-%dT%H:%M:%SZ") + "' AND "
                + "Program = '" + machine.name + "'").get_points())  # get all machine data in considered period
            last_traciability_code = machine.last_traciability_code
            last_production_time = datetime.strptime(machine.last_production_time, '%Y-%m-%dT%H:%M:%SZ')
            current_good_pieces, current_bad_pieces, error = 0, 0, False
            current_good_time, current_wasted_time = timedelta(seconds=0), timedelta(seconds=0)
            for data in rs:
                if len(data["time"]) == 22:  # if the time includes milliseconds
                    data["time"] = data["time"][:-3] + "Z"
                current_production_time = datetime.strptime(data["time"], '%Y-%m-%dT%H:%M:%SZ')
                diff_between_time = current_production_time - last_production_time
                if (diff_between_time > timedelta(seconds=machine.max_interval_same_piece) and data["Traciability_Code"] == last_traciability_code) \
                        or (diff_between_time > timedelta(seconds=machine.max_interval_different_pieces) and data["Traciability_Code"] != last_traciability_code):
                    current_wasted_time += diff_between_time
                else:
                    current_good_time += diff_between_time
                last_production_time = current_production_time
                if error is True and data["Traciability_Code"] == last_traciability_code:
                    continue
                elif last_traciability_code == data["Traciability_Code"]:
                    continue
                elif last_traciability_code != data["Traciability_Code"]:
                    current_good_pieces += 1
                    last_traciability_code = data["Traciability_Code"]
                    error = False
                if data["Error"] == 1:
                    current_bad_pieces += 1
                    error = True
        machine.last_production_time = last_production_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        print(current_good_time, current_wasted_time, current_good_pieces, current_bad_pieces)
        prev_time = new_time
    machine.last_production_time = prev_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    next_hour = (date + timedelta(hours=1)).replace(minute=0, second=0)  # to know which is the next hour
    second_to_wait = (next_hour - date).total_seconds()  # to know how many seconds we have to wait for the next period
    time.sleep(second_to_wait)  # sleep for waiting period
    date = datetime.now()  # set new time


def loadNewMachineFromFile():
    fp = open("prova.json", "r")
    x = json.loads(fp.read())
    mc = Machine.from_dict(x)
    machineController.storeMachine(mc)
