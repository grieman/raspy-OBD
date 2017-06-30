import obd
import pandas as pd

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

    rpm = connection.query(obd.connect.RPM)
    out_row = pd.Series([rpm.time, rpm.value])
    data = data.append()
    return data




connection = obd.OBD()
# ports = obd.scan_serial() 
# connection = obd.OBD("bluetooth port")
data = pd.DataFrame()
data = get_data(data)


