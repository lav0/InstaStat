import os
import sys
import json

from datetime import datetime
from numpy.random.mtrand import f
from mediaHolder import MediaHolder
from mediaHolder import user_media
from usersProvider import get_name_to_id_dict_from_db


user_dict = get_name_to_id_dict_from_db()

user_id = user_dict['lav_q']
all_media = user_media(user_id)
media_holders_list = list()

for media in all_media:
    media_holders_list.append(MediaHolder(media))

sorted_by_like = sorted(media_holders_list, key=lambda m: m.like_count(), reverse=True)

total_media_num = len(media_holders_list)
if total_media_num % 2 == 1:
    mean = sorted_by_like[total_media_num / 2].like_count()
else:
    left_mean = sorted_by_like[total_media_num / 2].like_count()
    right_mean = sorted_by_like[total_media_num / 2 - 1].like_count()
    mean = 0.5 * (left_mean + right_mean)

print 'mean   : ', mean
print 'average: ', sum([m.like_count() for m in media_holders_list]) / float(len(media_holders_list))

for p in sorted_by_like:
    print p.link(), p.like_count()



