from datetime import datetime
from datetime import timedelta
from usersProvider import get_name_to_id_dict_from_db
from authInfoProvider import get_access_token
from urlPrototypes import recentMediaUrlPrototype
from urlPrototypes import userUrlPrototype
from urlPrototypes import selfInfo
from urlPrototypes import selfFollowedBy
from urlPrototypes import selfFollows
from urlPrototypes import get_url
import urllib2
import string
import json
import os
import sys

self_id = None


def get_next_url(json_data):
    if isinstance(json_data, dict):
        if 'pagination' in json_data.keys():
            pag = json_data['pagination']
            if 'next_url' in pag.keys():
                return pag['next_url']
    return None


def get_self_url(access_token):
    return string.replace(selfInfo, "ACCESS-TOKEN", access_token)


def get_self_id():
    global self_id
    if self_id is not None:
        return self_id
    url = get_self_url(get_access_token())
    raw_data = urllib2.urlopen(url).read()
    json_data = json.loads(raw_data)
    self_id = int(json_data['data']['id'])
    return self_id


class DataUpdater:
    def __init__(self, access_token, user_id=None, user_name=None):
        self.user_id = None
        self.user_name = None
        self.__setup_user_id(user_id, user_name)
        if self.user_id is None:
            return
        self.access_token = access_token
        self.dir = 'users/' + str(self.user_id) + '/'
        self.date_file = self.dir + 'lastModifiedDate.txt'
        self.current_date = datetime.now()
        self.dynamic_data = self.dir + 'dynamicUserData.json'
        self.media_count = None
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    def __setup_user_id(self, user_id, user_name):
        if user_name is None:
            self.user_id = user_id
        else:
            self.user_name = user_name
            names_to_ids = get_name_to_id_dict_from_db()
            if user_name in names_to_ids.keys():
                self.user_id = names_to_ids[user_name]

    def is_update_allowed(self):
        if self.user_id is None:
            return False
        if not os.path.exists(self.date_file):
            return True
        str_date = open(self.date_file, 'r').read()
        last_modified = datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S.%f')
        return self.current_date - last_modified > timedelta(hours=12)

    def write_current_date(self):
        if self.user_id is None:
            return False
        open(self.date_file, 'w').write(str(self.current_date))

    def update_user_data(self):
        if self.user_id is None:
            return False
        print "Updating user data"
        data_url = get_url(self.user_id, self.access_token, userUrlPrototype)
        response = urllib2.urlopen(data_url)
        raw_data = response.read()
        filename = self.dir + "userData.json"
        f = open(filename, 'w')
        f.write(raw_data)
        f = open(filename)
        json_data = json.load(f)
        counts = json_data['data']['counts']
        self.media_count = counts['media']

        if not os.path.exists(self.dynamic_data):
            dyn_data = {str(self.current_date): counts}
        else:
            f_dynamic = open(self.dynamic_data, 'r')
            dyn_data = json.load(f_dynamic)
            dyn_data[str(self.current_date)] = counts

        f_dynamic = open(self.dynamic_data, 'w+')
        json.dump(dyn_data, f_dynamic, separators=(',\n', ':'))

    def update_media_data(self):
        if self.user_id is None:
            return False
        print "Updating media"
        data_url = get_url(self.user_id, self.access_token, recentMediaUrlPrototype)
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
            if self.media_count is not None:
                print int(100 * (len(data) / float(self.media_count))), "%"
            data_url = get_next_url(json_all)
        f.close()
        os.remove(filename)
        final_file = open(self.dir + "mediaData.json", 'w')
        json.dump(data, final_file)

    def __update_relationships(self, principle):
        if self.user_id is None:
            return False

        principle_to_url_prototype = {
            'followed_by': selfFollowedBy,
            'follows': selfFollows
        }

        if principle not in principle_to_url_prototype.keys():
            return

        if get_self_id() != self.user_id:
            # relationship info accessible for access-token owner only
            return

        print "Updating relationship:", principle

        ids_to_names_dictionary = dict()
        url = get_url('', get_access_token(), principle_to_url_prototype[principle])
        while url is not None:
            raw_data = urllib2.urlopen(url).read()
            json_data = json.loads(raw_data)
            users = json_data['data']
            list_of_dictionaries = [{entry['id']: entry['username']} for entry in users]
            for d in list_of_dictionaries:
                ids_to_names_dictionary.update(d)
            url = get_next_url(json_data)
        aim_directory = self.dir + principle + '/'
        if not os.path.exists(aim_directory):
            os.mkdir(aim_directory)
        final_file = open(aim_directory + str(datetime.now().date()) + '.json', 'w')
        json.dump(ids_to_names_dictionary, final_file)

    def update_followed_by(self):
        return self.__update_relationships('followed_by')

    def update_follows(self):
        return self.__update_relationships('follows')

    def update(self):
        if self.is_update_allowed():
            print "Updating user:", self.user_name if self.user_name is not None else self.user_id
            self.update_user_data()
            self.update_media_data()
            self.update_followed_by()
            self.update_follows()
            self.write_current_date()


def update(user_name=None):
    d = get_name_to_id_dict_from_db()
    if user_name in d.keys():
        updater = DataUpdater(user_id=d[user_name], access_token=get_access_token())
        updater.update()


def update_all():
    d = get_name_to_id_dict_from_db()
    for name in d.keys():
        updater = DataUpdater(user_name=name, access_token=get_access_token())
        updater.update()

arg = sys.argv[-1]
if arg == "all":
    update_all()
else:
    update(arg)


