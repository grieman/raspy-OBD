# make last week of data
# last_week
import tests
from datetime import datetime, timedelta
import os
import glob

def health(col = "rpm", data = last_week, upper_threshold, lower_threshold, upper_limit, cushion):
    column = data[col]
    _, num_outliers = tests.detect_outliers(column, tolerance=2)
    precision_change = tests.precision_loss(column)
    _, times_over, times_under = tests.out_of_range(column, upper_threshold, lower_threshold, cushion)
    _, _, stable_periods = tests.bad_signal(column, cushion)
    _, _, _, max_diff, mean_diff = tests.step_change(column)
    _, yhat_leading_crossed, yhat_crossed, yhat_trailing_crossed, interval_width = time_to_threshold(data["time", col], threshold=upper_limit, above=True)
    
    out_dict =  {col + "_num_outliers": num_outliers, 
                 col + "_precision_change":precision_change, 
                 col + "_times_over":times_over, 
                 col + "_times_under":times_under, 
                 col + "_stable_periods":stable_periods, 
                 col + "_max_diff":max_diff, 
                 col + "_mean_diff":mean_diff, 
                 col + "_yhat_leading_crossed":yhat_leading_crossed, 
                 col + "_yhat_crossed":yhat_crossed, 
                 col + "_yhat_trailing_crossed":yhat_trailing_crossed}
    return out_dict

# use to loop through all measurements
parameter_list = [["rpm", 3000, 1000, 4000, 3],
                  ["fuel", 0, 1, 1, 3]]


path = 'path/to/data/new'
os.chdir(path)
new_csvs = [i for i in glob.glob('*.csv')]

for dataset in new_csvs:
    new_data = pd.read_csv(dataset)
    datetimes = new_data["time"]

    ## Add to SQL table and remove from memory

    out_dataframe = pd.DataFrame()

    for date in datetimes:
        one_week_data = ## ingest data from SQL between date and one week prior

        ## Start with two columns - bookending the times analyzed
        start = date - timedelta(days = 7)
        end = date
        row_vec = {"Window Start":start, "Window End":end}
        for measurement in parameter_list:
            health_dict = health(measurement[0], one_week_data, measurement[1], measurement[2], measurement[3], 3)
            row_dict.update(health_dict)

    
    out_dataframe = out_dataframe.append(out_dict)

    # write to SQL


        
