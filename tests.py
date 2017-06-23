""" Intended to be imported and used as a module. Contains all tests run on data.
Data should be as pandas Series """

import pandas as pd
import numpy as np

def detect_outliers(data, tolerance=2):
    """ Finds outliers using local medians """
    medians = data.rolling(5, center=True).median()
    lowerq = data.rolling(5, center=True).quantile(.75)
    upperq = data.rolling(5, center=True).quantile(.25)
    iqrs = np.abs(upperq - lowerq)
    diffs = np.abs(data - medians)
    outliers = diffs > (tolerance * iqrs)
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
    return moving_average, diffs

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

#def remaining_useful_life(data, threshold):
#    """ Forecasts the remaining time before a threshold is crossed """
    