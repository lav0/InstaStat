from urlPrototypes import userUrlPrototype
from urlPrototypes import get_url
from authInfoProvider import get_access_token
import urllib2
from json import loads
import json
import os


def get_name_to_id_dict_from_db():
    dir_data = "data/ids.json"
    if not os.path.exists(dir_data):
        raise ValueError("No user ids provided")
    ids_file = open(dir_data, 'r')
    data = json.load(ids_file)
    if not isinstance(data, dict):
        raise ValueError("Bad ids file")
    return data


class UserInfoProvider:
    def __init__(self, user_id):
        self.id = user_id
        self.access_token = get_access_token()
        self.info = dict()
        self.__load_info()

    def __load_info(self):
        url = get_url(self.id, self.access_token, userUrlPrototype)
        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError:
            return
        except urllib2.URLError:
            return
        raw_data = response.read()
        data = loads(raw_data)
        if 'error_message' in data['meta'].keys():
            print data['meta']['error_message']
            return
        self.info.update(data['data'])

    def is_valid(self):
        return len(self.info) > 0

    def user_name(self):
        if 'username' in self.info.keys():
            return self.info['username']

    def profile_picture_url(self):
        if 'profile_picture' in self.info.keys():
            return self.info['profile_picture']

    def instagram_profile_url(self):
        name = self.user_name()
        if name is not None:
            return 'https://instagram.com/' + name

    def followers_count(self):
        if 'counts' in self.info.keys():
            return self.info['counts']['followed_by']

    def followings_count(self):
        if 'counts' in self.info.keys():
            return self.info['counts']['follows']

    def media_count(self):
        if 'counts' in self.info.keys():
            return self.info['counts']['media']

