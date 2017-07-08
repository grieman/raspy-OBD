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
try:
    while True:
        dataset = dataset.append(get_data(), ignore_index=True)
        print(dataset)
        # this ensures that the loop restarts every x=1.0 seconds. May need to be changed if execution becomes too lengthy
        time.sleep(1.0 - ((time.time() - starttime) % 1.0))
except KeyboardInterrupt:
    pass
