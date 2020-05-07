from Controller import machineController
from Controller.connection import influxDB
from datetime import datetime
from datetime import timedelta
from Model.machine import Machine
from Model.oee import OEE
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
date = datetime(year=2019, month=12, day=5, hour=23, minute=59, second=30, microsecond=0)

machines = machineController.getAllMachines()
prev_time = date.replace(hour=0, minute=0, second=0, microsecond=0)  # to obtain the first daily date

while len(machines) > 0:
    # setting the limit to the last calculable shift (xx:00:00)
    dateLimit = date.replace(minute=0, second=0, microsecond=0)

    # cycle till we have reach the limit previously calculated
    while prev_time < dateLimit:
        new_time = prev_time + timedelta(hours=1)
        print(f"\nStarting hour: {str(prev_time)} ---- Ending hour: {str(new_time)}")
        influx = influxDB()

        # foreach machine in db we're going to update relative oee
        for machine in machines:
            machine = machines[machine]
            toFind = ""
            for z in machine.program:
                toFind += f"Program = '{z}' OR "
            if len(toFind) == 0:
                continue
            else:
                toFind = toFind[:-4]
            rs = list(influx.query("SELECT * FROM prova4 WHERE time >= '{}' AND time < '{}' AND ({})".format(
                prev_time.strftime("%Y-%m-%dT%H:%M:%SZ"), new_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                toFind)).get_points())  # get all machine data in considered period
            if len(rs) > 0:
                first_production_time = datetime.strptime(rs[0]["time"], '%Y-%m-%dT%H:%M:%SZ')
                diff_between_time = first_production_time - prev_time
                if diff_between_time > timedelta(minutes=0):
                    current_good_time = timedelta(seconds=0)
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
                last_traciability_code = machine.last_traciability_code
                if len(data["time"]) == 22:  # if the time includes milliseconds
                    data["time"] = data["time"][:-3] + "Z"
                current_production_time = datetime.strptime(data["time"], '%Y-%m-%dT%H:%M:%SZ')
                diff_between_time = current_production_time - last_production_time
                if (diff_between_time > timedelta(seconds=machine.max_interval_same_piece) and data[
                    "Traciability_Code"] == last_traciability_code) \
                        or (diff_between_time > timedelta(seconds=machine.max_interval_different_pieces) and data[
                    "Traciability_Code"] != last_traciability_code):
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
                    machine.last_traciability_code = data["Traciability_Code"]
                    error = False
                if data["Error"] == 1:
                    current_bad_pieces += 1
                    error = True

            # adding the last off shift to complete the period and update the last production time
            machine.last_production_time = new_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            machine.last_available_oee = str(prev_time)

            # declare a new OEE object about the current period and add it to the machine
            oee = OEE(good_pieces=current_good_pieces, bad_pieces=current_bad_pieces)
            if current_good_time.total_seconds() + current_wasted_time.total_seconds() > 0 and current_good_pieces + current_bad_pieces > 0:
               #  lo stato della macchina viene calcolato sulla base della disponibilità
                oee.availability = round(current_good_time.total_seconds() / (
                        current_good_time.total_seconds() + current_wasted_time.total_seconds()) * 100, 2)
                oee.performance = round(machine.cycle_time * current_good_pieces / current_good_time.total_seconds() * 100, 2)
                oee.quality = round(current_good_pieces / (current_bad_pieces + current_good_pieces) * 100, 2)
                oee.general = round(oee.availability * oee.performance * oee.quality / 10000, 2)
            else:
                oee.availability = 0
                oee.performance = 0
                oee.quality = 0
                oee.general = 0
            if oee.availability == 0:
                oee.status = "off"
            elif oee.availability < 30:
                oee.status = "error"
            elif oee.availability < 50:
                oee.status = "warning"
            else:
                oee.status = "run"
            machine.addOEE(oee, str(prev_time))
            machineController.updateMachineStatus(machine)  # update machine data

            # info print
            print(
                f"{machine.name} ---- {bcolors.OKBLUE}Products OK: {oee.good_pieces}, {bcolors.FAIL}Products KO: {oee.bad_pieces}, {bcolors.OKBLUE}Running time: {current_good_time}, {bcolors.FAIL}Wasted time: {current_wasted_time}{bcolors.ENDC} -- Status: {oee.status}")
        # increment
        prev_time = new_time

    # once we have loaded all the older period, we can update data and wait for the next period
    next_hour = (date + timedelta(hours=1)).replace(minute=0, second=0)  # to know which is the next hour
    second_to_wait = (next_hour - date).total_seconds()  # to know how many seconds we have to wait for the next period
    time.sleep(second_to_wait)  # sleep for waiting period
    date = datetime.now()  # set new time



def loadNewMachineFromFile():
    fp = open("machine_example.json", "r")
    x = json.loads(fp.read())
    mc = Machine.from_dict(x)
    machineController.storeMachine(mc)