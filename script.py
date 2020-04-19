from Controller import machineController
from Controller.connection import influxDB
from datetime import datetime
from datetime import timedelta
from Model.machine import Machine
from Model.oee import OEE
from Model.hour_detail import HourDetail
import time
import json


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# for simulating purpose we define actual time, in future this date it's now date
date = datetime(year=2019, month=12, day=5, hour=20, minute=30, second=0, microsecond=0)

machines = machineController.getAllMachines()
prev_time = date.replace(hour=0, minute=0, second=0, microsecond=0)  # to obtain the first daily date

while len(machines) > 0:
    # setting the limit to the last calculable shift (xx:00:00)
    dateLimit = date.replace(minute=0, second=0, microsecond=0)

    # cycle till we have reach the limit previously calculated
    while prev_time <= dateLimit:
        new_time = prev_time + timedelta(hours=1)
        print(f"\n{bcolors.WARNING}Starting hour: {str(prev_time)} ---- Ending hour: {str(new_time)}{bcolors.ENDC}")
        influx = influxDB()

        # foreach machine in db we're going to update relative oee
        for machine in machines:
            machine = machines[machine]
            list_hour_detail = list()
            rs = list(influx.query(
                "SELECT * FROM prova4 WHERE time >= '" + prev_time.strftime("%Y-%m-%dT%H:%M:%SZ") + "' AND "
                + "time < '" + new_time.strftime("%Y-%m-%dT%H:%M:%SZ") + "' AND "
                + "Program = '" + machine.name + "'").get_points())  # get all machine data in considered period
            if len(rs) > 0:
                first_production_time = datetime.strptime(rs[0]["time"], '%Y-%m-%dT%H:%M:%SZ')
                diff_between_time = first_production_time - prev_time
                if diff_between_time > timedelta(minutes=0):
                    current_good_time = timedelta(seconds=0)
                    x = HourDetail(status="off", startHour=prev_time, endHour=first_production_time)
                    list_hour_detail.append(x)
                    machine.last_production_time = rs[0]["time"]
                else:
                    current_good_time = timedelta(seconds=0)
            else:
                current_good_time = timedelta(seconds=0)
            last_traciability_code = machine.last_traciability_code
            last_production_time = datetime.strptime(machine.last_production_time, '%Y-%m-%dT%H:%M:%SZ')
            current_good_pieces, current_bad_pieces, error = 0, 0, False
            current_wasted_time = timedelta(seconds=0)
            x = None
            for data in rs:
                if len(data["time"]) == 22:  # if the time includes milliseconds
                    data["time"] = data["time"][:-3] + "Z"
                current_production_time = datetime.strptime(data["time"], '%Y-%m-%dT%H:%M:%SZ')
                diff_between_time = current_production_time - last_production_time
                if (diff_between_time > timedelta(seconds=machine.max_interval_same_piece) and data[
                    "Traciability_Code"] == last_traciability_code) \
                        or (diff_between_time > timedelta(seconds=machine.max_interval_different_pieces) and data[
                    "Traciability_Code"] != last_traciability_code):
                    current_wasted_time += diff_between_time
                    if x is not None:
                        x.endHour = last_production_time
                        list_hour_detail.append(x)
                    x = HourDetail(status="delay", startHour=last_production_time, endHour=current_production_time)
                    list_hour_detail.append(x)
                    x = None
                else:
                    if x is None:  # significa che ancora non è stato impostato l'orario di inizio turno "positivo"
                        x = HourDetail(status="run", startHour=current_production_time,
                                       endHour=None)  # non so a che ora finisce però il turno "positivo"
                    if data == rs[-1]:
                        x.endHour = current_production_time
                        list_hour_detail.append(x)
                        x = None
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

        # adding the last off shift to complete the period and update the last production time
        x = HourDetail(status="off", startHour=last_production_time, endHour=new_time)
        list_hour_detail.append(x)
        machine.last_production_time = new_time.strftime('%Y-%m-%dT%H:%M:%SZ')

        # declare a new OEE object about the current period and add it to the machine
        oee = OEE(good_pieces=current_good_pieces, bad_pieces=current_bad_pieces, hour_detail=list_hour_detail)
        machine.addOEE(oee, str(prev_time))

        # info print
        print(f"{bcolors.OKBLUE}Products OK: {oee.good_pieces}, Products KO: {oee.bad_pieces}, Wasted time: {current_wasted_time}, Running time: {current_good_time}")

        # increment
        prev_time = new_time

    # once we have loaded all the older period, we can update data and wait for the next period
    machineController.updateMachineStatus(machine)  # update machine data
    next_hour = (date + timedelta(hours=1)).replace(minute=0, second=0)  # to know which is the next hour
    second_to_wait = (next_hour - date).total_seconds()  # to know how many seconds we have to wait for the next period
    time.sleep(second_to_wait)  # sleep for waiting period
    date = datetime.now()  # set new time


def loadNewMachineFromFile():
    fp = open("prova.json", "r")
    x = json.loads(fp.read())
    mc = Machine.from_dict(x)
    machineController.storeMachine(mc)
