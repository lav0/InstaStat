import urllib2
import string
from datetime import datetime
from datetime import timedelta
import json
import os

recentMediaUrlPrototype = \
    "https://api.instagram.com/v1/users/{user-id}/media/recent/?access_token=ACCESS-TOKEN"
userUrlPrototype = \
    "https://api.instagram.com/v1/users/{user-id}/?access_token=ACCESS-TOKEN"


def get_auth_token(token):
    dir_data = "data/auth.json"
    if not os.path.exists(dir_data):
        raise ValueError(token + " is not provided. Put in 'data/auth.json' !")
    auth_file = open(dir_data, 'r')
    data = json.load(auth_file)
    value = str(data[token])
    if not isinstance(data, dict):
        raise ValueError(token + " is not provided. Put in 'data/auth.json' !!")
    return value


def get_access_token():
    return get_auth_token(u'AccessToken')


def get_client_id():
    return get_access_token("ClientID")


def get_client_secret():
    return get_access_token("ClientSecret")


def name_to_id_dict():
    dir_data = "data/ids.json"
    if not os.path.exists(dir_data):
        raise ValueError("No user ids provided")
    ids_file = open(dir_data, 'r')
    data = json.load(ids_file)
    if not isinstance(data, dict):
        raise ValueError("Bad ids file")
    return data


def get_url(user_id, access_token, prototype=recentMediaUrlPrototype):
    tmp = string.replace(prototype, '{user-id}', str(user_id))
    return string.replace(tmp, "ACCESS-TOKEN", access_token)


def get_next_url(json_data):
    if isinstance(json_data, dict):
        if 'pagination' in json_data.keys():
            pag = json_data['pagination']
            if 'next_url' in pag.keys():
                return pag['next_url']
    return None


class DataUpdater:
    def __init__(self, user_id, access_token):
        self.user_id = user_id
        self.access_token = access_token
        self.dir = str(user_id) + '/'
        self.date_file = self.dir + 'lastModifiedDate.txt'
        self.current_date = datetime.now()
        self.dynamic_data = self.dir + 'dynamicUserData.json'
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    def is_update_allowed(self):
        if not os.path.exists(self.date_file):
            return True
        str_date = open(self.date_file, 'r').read()
        last_modified = datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S.%f')
        return self.current_date - last_modified > timedelta(hours=12)

    def write_current_date(self):
        open(self.date_file, 'w').write(str(self.current_date))

    def update_user_data(self):
        data_url = get_url(self.user_id, self.access_token, userUrlPrototype)
        response = urllib2.urlopen(data_url)
        raw_data = response.read()
        filename = self.dir + "userData.json"
        f = open(filename, 'w')
        f.write(raw_data)
        f = open(filename)
        json_data = json.load(f)
        counts = json_data['data']['counts']

        if not os.path.exists(self.dynamic_data):
            dyn_data = {str(self.current_date): counts}
        else:
            f_dynamic = open(self.dynamic_data, 'r')
            dyn_data = json.load(f_dynamic)
            dyn_data[str(self.current_date)] = counts

        f_dynamic = open(self.dynamic_data, 'w+')
        json.dump(dyn_data, f_dynamic, separators=(',\n', ':'))

    def update_media_data(self):
        data_url = get_url(self.user_id, self.access_token)
        data = list()
        filename = "__tmpFile"
        f = open(filename, 'w')
        while data_url is not None:
            response = urllib2.urlopen(data_url)
            raw_data = response.read()
            f = open(filename, 'w')
            f.write(raw_data)
            f = open(filename, 'r')
            json_all = json.load(f)
            data += json_all['data']
            print len(data)
            data_url = get_next_url(json_all)
        f.close()
        os.remove(filename)
        final_file = open(self.dir + "mediaData.json", 'w')
        json.dump(data, final_file)

    def update(self):
        if self.is_update_allowed():
            self.update_user_data()
            self.update_media_data()
            self.write_current_date()


def update_all():
    d = name_to_id_dict()
    for userid in d.values():
        DataUpdater(userid, get_access_token()).update()

update_all()
