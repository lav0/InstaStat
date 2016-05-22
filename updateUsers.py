import json
import sys
import os
from instagram.client import InstagramAPI
import authInfoProvider


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


api = InstagramAPI(
                    client_id=authInfoProvider.get_client_id(),
                    client_secret=authInfoProvider.get_client_secret()
                   )

target_name = sys.argv[-1]

result = api.user_search(target_name)
user = [p for p in result if p.username == target_name]
if user:
    user = user[0]
else:
    print "User not found."

print "Found user:", user.username
userid = save_user(user.username, user.id)


from updateData import DataUpdater

DataUpdater(userid, authInfoProvider.get_access_token()).update()


