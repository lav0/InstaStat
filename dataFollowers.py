import os
import json
import re
from datetime import datetime
from datetime import timedelta


###############################################################################
def get_aim_path(principle):
    if os.path.exists('users/'):
        for x in os.walk('users/'):
            if principle in x[1]:
                return x[0] + '/followed_by'
    return None


###############################################################################
def build_dates_to_filename_dict(aim_path):
    dates_to_filenames = dict()
    files = os.listdir(aim_path)
    for file_name in files:
        str_date, str_ext = os.path.splitext(file_name)
        if str_ext != '.json':
            continue
        date_checker = re.compile('^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$')
        if date_checker.match(str_date) is None:
            continue
        dates_to_filenames[datetime.strptime(str_date, '%Y-%m-%d')] = file_name

    return dates_to_filenames


###############################################################################
def compared_files_with_period(period_days=1, principle='followed_by'):
    if principle not in ['followed_by']: #, 'following']:
        return None

    aim_path = get_aim_path(principle)

    if aim_path is None:
        print 'No directory for', principle

    dates_to_filenames = build_dates_to_filename_dict(aim_path)

    if len(dates_to_filenames) <= 1:
        print 'Not enough statistics collected'
        return None

    period = timedelta(days=period_days)
    last_date = dates_to_filenames.keys()[-1]
    for prev_date in dates_to_filenames.keys()[-2::-1]:
        if last_date - prev_date >= period:
            return aim_path + '/' + dates_to_filenames[prev_date], \
                   aim_path + '/' + dates_to_filenames[last_date]

    return None


file1, file2 = compared_files_with_period(period_days=1)
data1 = json.load(open(file1, 'r'))
data2 = json.load(open(file2, 'r'))

for key in data1.keys():
    if key not in data2.keys():
        print "Unfollowed: ", data1[key]

for key in data2.keys():
    if key not in data1.keys():
        print "New follow: ", data2[key]
