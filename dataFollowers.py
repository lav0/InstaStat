import os
import json
import re
from datetime import datetime
from datetime import timedelta

regex_date_pattern = '^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$'


###############################################################################
def get_aim_path(principle):
    if os.path.exists('users/'):
        for x in os.walk('users/'):
            if principle in x[1]:
                return x[0] + '/' + principle
    return None


###############################################################################
def build_dates_to_filename_dict(aim_path):
    date_checker = re.compile(regex_date_pattern)
    dates_to_filenames = dict()
    files = os.listdir(aim_path)
    for file_name in files:
        str_date, str_ext = os.path.splitext(file_name)
        if str_ext != '.json':
            continue
        if date_checker.match(str_date) is None:
            continue
        dates_to_filenames[datetime.strptime(str_date, '%Y-%m-%d')] = file_name

    return dates_to_filenames


###############################################################################
def relationship_data_for_period(period_days=1, principle='followed_by'):
    if principle not in ['followed_by', 'follows']:
        return None

    aim_path = get_aim_path(principle)

    if aim_path is None:
        print 'No directory for', principle

    dates_to_filenames = build_dates_to_filename_dict(aim_path)

    period = timedelta(days=period_days)

    now = datetime.now()
    result = list()
    for date in dates_to_filenames.keys():
        if now - date <= period:
            result += json.load(open(aim_path + '/' + dates_to_filenames[date]))

    return result


###############################################################################
def relationship_data_the_last(principle='followed_by'):
    if principle not in ['followed_by', 'follows']:
        return None

    aim_path = get_aim_path(principle)

    if aim_path is None:
        print 'No directory for', principle

    dates_to_filenames = build_dates_to_filename_dict(aim_path)

    #
    # I can assume the files to be already sorted according to the names
    # and, consequently, to the dates when data was acquired on
    # however, let's be sure we're getting the last (newest) one
    #
    the_last = sorted(dates_to_filenames.keys())[-1]

    return json.load(open(aim_path + '/' + dates_to_filenames[the_last]))


# the complement operation of sets ############################################
def list_subtraction(minuend_list, subtrahend_list):
    result = list()
    for entry in minuend_list:
        if entry not in subtrahend_list:
            result.append(entry)
    return result


###############################################################################
def print_the_ones_i_dont_follow_back():
    followers = relationship_data_the_last(principle='followed_by')
    followings = relationship_data_the_last(principle='follows')

    pours = list_subtraction(followers, followings)
    print "There are", len(pours), "Followers you don't follow back: "
    for p in pours:
        print followers[p]


###############################################################################
def print_the_ones_who_dont_follow_me_back():
    followers = relationship_data_the_last(principle='followed_by')
    followings = relationship_data_the_last(principle='follows')

    toughs = list_subtraction(followings, followers)
    print "There are", len(toughs), "Following users who don't follow you back: "
    for p in toughs:
        print followings[p]

print_the_ones_who_dont_follow_me_back()

# file1, file2 = compared_files_with_period(period_days=3, principle='followed_by')
# data1 = json.load(open(file1, 'r'))
# data2 = json.load(open(file2, 'r'))
#
# something_shawn = False
# for key in data1.keys():
#     if key not in data2.keys():
#         print "Unfollowed: ", data1[key]
#         something_shawn = True
#
# for key in data2.keys():
#     if key not in data1.keys():
#         print "New follow: ", data2[key]
#         something_shawn = True
#
# if not something_shawn:
#     print len([x for x in data1.values()])
