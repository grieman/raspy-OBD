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
    outlist =  [num_outliers, precision_change, times_over, times_under, stable_periods, max_diff, mean_diff, yhat_leading_crossed, yhat_crossed, yhat_trailing_crossed]
    # name outlist?
    return outlist

# use to loop through all measurements
parameter_dict = {rpm:["rpm", 3000, 1000, 4000, 3]}


path = 'path/to/data/new'
os.chdir(path)
new_csvs = [i for i in glob.glob('*.csv')]

for dataset in new_csvs:
    new_data = pd.read_csv(dataset)

    ## Add to SQL table

    one_week_prior = new_data["time"] - timedelta(days=7)
    #thirty_days_prior = new_data["time"] - timedelta(days=30)

    for date in one_week_prior:
        one_week_data = ## data from SQL

        start = date
        end = date + timedelta(days = 7)
        rpm_out = health("rpm", one_week_data, 3000, 1000, 4000, 3])

        #concatenate start, end, *_outs
        # save as new row

        
