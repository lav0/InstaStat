
from datetime import datetime

class MediaHolder:
    def __init__(self, media_list):
        self.media = media_list

    def created_time(self):
        return datetime.fromtimestamp(float(self.media['created_time']))

    def like_count(self):
        return self.media['likes']['count']
