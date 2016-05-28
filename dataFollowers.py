import os
import json
import re
from datetime import datetime
from datetime import timedelta
from usersProvider import UserInfoProvider

regex_date_pattern = '^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$'


###############################################################################
def get_aim_path(principle):
    if principle not in ['followed_by', 'follows']:
        return None

    aim_path = None

    if os.path.exists('users/'):
        for x in os.walk('users/'):
            if principle in x[1]:
                aim_path = x[0] + '/' + principle

    if aim_path is None:
        print 'No directory for', principle

    return aim_path


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
    aim_path = get_aim_path(principle)

    dates_to_filenames = build_dates_to_filename_dict(aim_path)

    period = timedelta(days=period_days)

    now = datetime.now()
    result = dict()
    for date in dates_to_filenames.keys():
        if now - date <= period:
            file_path = aim_path + '/' + dates_to_filenames[date]
            result.update(json.load(open(file_path)))

    return result


###############################################################################
def relationship_data_the_last(principle='followed_by'):
    aim_path = get_aim_path(principle)

    dates_to_filenames = build_dates_to_filename_dict(aim_path)

    #
    # I can assume the files to be already sorted according to the names
    # and, consequently, to the dates when data was acquired on
    # however, let's be sure we're getting the last (newest) one
    #
    the_last = sorted(dates_to_filenames.keys())[-1]

    file_path = aim_path + '/' + dates_to_filenames[the_last]
    return json.load(open(file_path))


# the complement operation of sets ############################################
def list_subtraction(minuend_list, subtrahend_list):
    result = list()
    for entry in minuend_list:
        if entry not in subtrahend_list:
            result.append(entry)
    return result


###############################################################################
def get_the_ones_i_dont_follow_back():
    followers = relationship_data_the_last(principle='followed_by')
    followings = relationship_data_the_last(principle='follows')
    pours = list_subtraction(followers.keys(), followings.keys())
    return {p: followers[p] for p in pours}


###############################################################################
def get_the_ones_who_dont_follow_me_back():
    followers = relationship_data_the_last(principle='followed_by')
    followings = relationship_data_the_last(principle='follows')
    toughs = list_subtraction(followings.keys(), followers.keys())
    return {t: followings[t] for t in toughs}


###############################################################################
def get_lost_followers_for_period(period=7):
    followers = relationship_data_the_last(principle='followed_by')
    all_followers_in_period = \
        relationship_data_for_period(period_days=period, principle='followed_by')
    fagots = list_subtraction(all_followers_in_period.keys(), followers.keys())
    return {f: all_followers_in_period[f] for f in fagots}


###############################################################################
def print_the_ones_i_dont_follow_back():
    the_ones = get_the_ones_i_dont_follow_back()
    print "There are", len(the_ones), "Followers you don't follow back: "
    for p in the_ones.values():
        print p


###############################################################################
def print_the_ones_who_dont_follow_me_back():
    the_ones = get_the_ones_who_dont_follow_me_back()
    print "There are", len(the_ones), "Following users who don't follow you back: "
    for p in the_ones.values():
        print p


###############################################################################
def print_lost_followers_for_period(period=7):
    the_ones = get_lost_followers_for_period(period)
    print "There are", len(the_ones), "people who unfollowed you in last", period, "days."
    for fag in the_ones:
        print fag


lost = get_lost_followers_for_period()

for user_id in lost:
    provider = UserInfoProvider(user_id)
    print provider.instagram_profile_url()
