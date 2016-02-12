import json
import sys
import os
from instagram.client import InstagramAPI
from authInfoProvider import get_access_token
from authInfoProvider import get_client_id
from authInfoProvider import get_client_secret
from updateData import DataUpdater


def save_user(username, userid):
    dir_data = "data/"
    if not os.path.exists(dir_data):
        os.mkdir(dir_data)
    dir_data += "ids.json"
    data = dict()
    if os.path.exists(dir_data):
        ids_file = open(dir_data, 'r')
        data = json.load(ids_file)
    ids_file = open(dir_data, 'w')
    data[username] = int(userid)
    json.dump(data, ids_file)
    return data[username]


api = InstagramAPI(client_id=get_client_id(), client_secret=get_client_secret())

target_name = sys.argv[-1]

result = api.user_search(target_name)
user = [p for p in result if p.username == target_name]
if user:
    user = user[0]
else:
    print "User not found."

print "Found user:", user.username
userid = save_user(user.username, user.id)

DataUpdater(userid, get_access_token()).update()


