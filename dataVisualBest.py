import os
import sys
import json

from datetime import datetime
from numpy.random.mtrand import f
from mediaHolder import MediaHolder
from mediaHolder import user_media
from usersProvider import name_to_id_dict


user_dict = name_to_id_dict()

user_id = user_dict['brenton_clarke']
all_media = user_media(user_id)
media_holders_list = list()

for media in all_media:
    media_holders_list.append(MediaHolder(media))

sorted_by_like = sorted(media_holders_list, key=lambda m: m.like_count(), reverse=True)

for p in sorted_by_like:
    print p.link()



