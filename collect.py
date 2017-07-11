import obd
import pandas as pd
import time

def get_data():
    # rpm = obd.commands.RPM
    # fuel = obd.commands.FUEL_STATUS
    # coolant = obd.commands.COOLANT_TEMP
    # speed = obd.commands.SPEED
    # intake = obd.commands.INTAKE_STATUS
    # run_time = obd.commands.RUN_TIME
    # throttle = obd.commands.THROTTLE_POS
    # fuel_press = obd.commands.FUEL_PRESSURE
    # intake_press = obd.commands.INTAKE_PRESSURE
    # air_flow_rate = obd.commands.MAF
    # ambiant_temp = obd.commands.AMBIANT_AIR_TEMP
    # ethanol = obd.commands.ETHANOL_PERCENT
    # oil_temp = obd.commands.OIL_TEMP
    # fuel_consumption = obd.commands.FUEL_RATE
    rpm = connection.query(obd.commands.RPM)
    out_row = pd.Series([rpm.time, rpm.value])
    return out_row




connection = obd.OBD()
# ports = obd.scan_serial() 
# connection = obd.OBD("bluetooth port")

dataset = pd.DataFrame()
starttime = time.time()
car_on = False

try:
  while True:
    print(dataset)
    next_row = get_data()
    if car_on:
      time.sleep(1.0 - ((time.time() - starttime) % 1.0))
      dataset = dataset.append(next_row, ignore_index=True)
      if next_row[1] < 1:
        car_on = False
        # save as csv
    else:
      time.sleep(10.0 - ((time.time() - starttime) % 10.0))
      if next_row[1] > 0:
        car_on = True
        dataset = pd.DataFrame().append(next_row, ignore_index=True)
except KeyboardInterrupt:
    pass