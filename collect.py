import obd
import pandas as pd
import time

def get_data():
    rpm = connection.query(obd.commands.RPM)
    fuel = connection.query(obd.commands.FUEL_STATUS)
    coolant = connection.query(obd.commands.COOLANT_TEMP)
    speed = connection.query(obd.commands.SPEED)
    intake = connection.query(obd.commands.INTAKE_STATUS)
    run_time = connection.query(obd.commands.RUN_TIME)
    throttle = connection.query(obd.commands.THROTTLE_POS)
    fuel_press = connection.query(obd.commands.FUEL_PRESSURE)
    intake_press = connection.query(obd.commands.INTAKE_PRESSURE)
    air_flow_rate = connection.query(obd.commands.MAF)
    ambiant_temp = connection.query(obd.commands.AMBIANT_AIR_TEMP)
    ethanol = connection.query(obd.commands.ETHANOL_PERCENT)
    oil_temp = connection.query(obd.commands.OIL_TEMP)
    fuel_consumption = connection.query(obd.commands.FUEL_RATE)
    
    out_row = pd.Series([rpm.time, rpm.value, fuel.value, coolant.value,
          speed.value, intake.value, run_time.value, throttle.value, fuel_press.value,
          intake_press.value, air_flow_rate.value, ambiant_temp.value, ethanol.value,
          oil_temp.value, fuel_consumption.value])
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
        filename = "data/" + time.asctime(time.localtime(next_row[0])) + ".csv"
        dataset.to_csv(filename, sep="|")
    else:
      time.sleep(20.0 - ((time.time() - starttime) % 20.0))
      if next_row[1] > 0:
        car_on = True
        dataset = pd.DataFrame().append(next_row, ignore_index=True)
except KeyboardInterrupt:
    pass
