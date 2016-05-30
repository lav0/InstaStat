from mediaHolder import MediaHolder
from mediaHolder import user_media
from usersProvider import get_name_to_id_dict_from_db


class SortedMediaProvider:
    def __init__(self, user_id=None, user_name=None):
        self.user_id = None
        if user_id is not None:
            self.user_id = user_id
        elif user_name is not None:
            user_dict = get_name_to_id_dict_from_db()
            if user_name in user_dict.keys():
                self.user_id = user_dict[user_name]

        self.principle_to_media_holder_dict = dict()

    def is_defined(self):
        return self.user_id is not None

    def __make_sorted_media_by(self, principle):
        if not self.is_defined():
            print "Sorted media not defined."
            return False

        all_media = user_media(self.user_id)
        if all_media is None:
            print "User media not collected"
            return False

        media_holders_list = list()

        for media in all_media:
            media_holders_list.append(MediaHolder(media))

        sorted_media = sorted(media_holders_list, key=lambda m: m.like_count(), reverse=True)

        self.principle_to_media_holder_dict[principle] = sorted_media

        return True

    def get_media_sorted_by(self, principle):
        if principle not in self.principle_to_media_holder_dict.keys():
            fine = self.__make_sorted_media_by(principle)
            if not fine:
                return list()

        return self.principle_to_media_holder_dict[principle]

    def get_media_mean_value_for(self, principle):
        sorted_media = self.get_media_sorted_by(principle)

        total_media_num = len(sorted_media)
        if total_media_num % 2 == 1:
            mean = sorted_media[total_media_num / 2].like_count()
        else:
            left_mean = sorted_media[total_media_num / 2].like_count()
            right_mean = sorted_media[total_media_num / 2 - 1].like_count()
            mean = 0.5 * (left_mean + right_mean)

        return mean

    def get_media_average_value_fro(self, principle):
        sorted_media = self.get_media_sorted_by(principle)
        return sum([m.like_count() for m in sorted_media]) / float(len(sorted_media))


provider = SortedMediaProvider(user_name='tlmnva0')
sorted_by_like = provider.get_media_sorted_by('like_count')
for p in sorted_by_like:
    print p.link(), p.like_count()

print "Mean val:", provider.get_media_mean_value_for('like_count')
print "Average:", provider.get_media_average_value_fro('like_count')



