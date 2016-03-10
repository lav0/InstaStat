import os
import json
from datetime import datetime


class MediaHolder:
    def __init__(self, media_list):
        self.media = media_list

    def created_time(self):
        return datetime.fromtimestamp(float(self.media['created_time']))

    def like_count(self):
        return self.media['likes']['count']

    def link(self):
        return self.media['link']

    def image_std(self):
        return self.media['images']['standard_resolution']['url']


def user_media(userid):
    dir_data = 'users/' + str(userid) + '/mediaData.json'
    if not os.path.exists(dir_data):
        return None
    file_data = open(dir_data, 'r')
    json_data = json.load(file_data)
    return json_data