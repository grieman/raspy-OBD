""" Intended to be imported and used as a module. Contains all tests run on data.
Data should be as pandas Series """

import pandas as pd
import numpy as np
from fbprophet import Prophet

def detect_outliers(data, tolerance=2):
    """ Finds outliers using local medians """
    medians = data.rolling(5, center=True).median()
    lowerq = data.rolling(5, center=True).quantile(.75)
    upperq = data.rolling(5, center=True).quantile(.25)
    iqrs = np.abs(upperq - lowerq)
    diffs = np.abs(data - medians)
    outliers = pd.Series(diffs > (tolerance * iqrs))
    return outliers, sum(outliers)

def precision_loss(data): #singular value
    """ Compares standard deviations at start and end of series for difference """
    start = np.std(data.head(round(len(data)/8)))
    end = np.std(data.tail(round(len(data)/8)))
    change = end/start
    return change

def out_of_range(data, upper_threshold, lower_threshold, cushion=3):
    """ Checks readings against defined upper and lower bounds. Returns which points outside bounds
    and how often data crosses with at least *cushion* consecutive points out of bounds """
    above = (data > upper_threshold) * 1  # *1 --> int
    below = (data < lower_threshold) * 1
    out = above + (below * -1)

    index_backdown = [i + 1 for i, x in enumerate(np.diff(above)) if x == -1]
    step_down = np.diff(np.concatenate(([0.], np.cumsum(above)[index_backdown])))
    above[index_backdown] = -step_down
    test_above = np.cumsum(above)
    times_over = sum(test_above == cushion)

    index_backup = [i + 1 for i, x in enumerate(np.diff(below)) if x == -1]
    step_up = np.diff(np.concatenate(([0.], np.cumsum(below)[index_backup])))
    below[index_backup] = -step_up
    test_below = np.cumsum(below)
    times_under = sum(test_below == cushion)

    return out, times_over, times_under

def bad_signal(data, cushion=3):
    """ Checks for repeated signal """
    no_changes = stable = (np.diff(data) == 0) * 1
    change = [i + 1 for i, x in enumerate(np.diff(no_changes)) if x == -1]
    change_size = np.diff(np.concatenate(([0.], np.cumsum(no_changes)[change])))
    no_changes[change] = -change_size
    time_stable = np.cumsum(no_changes)
    stable_periods = sum(time_stable == cushion)
    return stable, time_stable, stable_periods

def step_change(data, span=10, lag=1):
    """ Checks data points against moving average to detect jumps """
    moving_average = data.ewm(span=span).mean()
    lagged = pd.Series(np.append(np.repeat(np.nan, lag), moving_average[:len(moving_average)-lag]))
    diffs = data[lag:] - lagged
    pct_diff = diffs/moving_average
    max_diff = max(pct_diff)
    mean_diff = np.mean(pct_diff)
    return moving_average, diffs, pct_diff, max_diff, avg_diff

def check_threshold(data, threshold, above=True, flexibility=.02, cushion=3):
    """ Checks if threshold has been exceeded """
    if above:
        across = (data > threshold) * 1
        across_secondary = (data > (threshold * (1-flexibility))) * 1
    else:
        across = (data < threshold) * 1
        across_secondary = (data < (threshold * (1+flexibility))) * 1

    index_backdown = [i + 1 for i, x in enumerate(np.diff(across_secondary)) if x == -1]
    step_down = np.diff(np.concatenate(([0.], np.cumsum(across)[index_backdown])))
    across[index_backdown] = -step_down
    test_across = np.cumsum(across)
    times_across = sum(test_across == cushion)

    return across, test_across, times_across

def time_to_threshold(data, threshold, above=True, forecast_length=3600, interval_width=.95):
    """ Forecasts the remaining time before a threshold is crossed """
    # needs other input format: dataframe with two columns, ds and y
    model = Prophet(interval_width=interval_width)
    try:
        data.columns = ['ds', 'y']
        model.fit(data)
    except:
        print("Input must be two columns: a date/time (string) column and a value (numeric) column")
        raise

    future_dates = model.make_future_dataframe(periods=forecast_length)
    forecast = model.predict(future_dates)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    if above:
        yhat_crossed = forecast["yhat"][forecast["yhat"] > threshold]
        yhat_leading_crossed = forecast["yhat_upper"][forecast["yhat_upper"] > threshold]
        yhat_trailing_crossed = forecast["yhat_lower"][forecast["yhat_lower"] > threshold]
    else:
        yhat_crossed = forecast["yhat"][forecast["yhat"] < threshold]
        yhat_leading_crossed = forecast["yhat_upper"][forecast["yhat_upper"] < threshold]
        yhat_trailing_crossed = forecast["yhat_lower"][forecast["yhat_lower"] < threshold]

    outlist = [yhat_crossed, yhat_leading_crossed, yhat_trailing_crossed]
    for i, _ in enumerate(outlist):
        if outlist[i].empty:
            outlist[i] = forecast_length
        else:
            outlist[i] = outlist[i].index[0]

    yhat_crossed = forecast['ds'][outlist[0]]
    yhat_leading_crossed = forecast['ds'][outlist[1]]
    yhat_trailing_crossed = forecast['ds'][outlist[2]]

    return forecast["yhat"], yhat_leading_crossed, yhat_crossed, yhat_trailing_crossed, interval_width
