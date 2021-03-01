import os

from types import SimpleNamespace


def find_latest_log(prefix):
    log_file = None
    max_x = 0
    for f in os.listdir('.'):
        if f.startswith(prefix):
            x = int(f.split('_')[2][:-4])
            if x > max_x:
                max_x = x
                log_file = f
    print('Latest log file: {}'.format(log_file))
    return log_file
