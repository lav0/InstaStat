from mediaHolder import MediaHolder
from mediaHolder import user_media
from usersProvider import get_name_to_id_dict_from_db


def get_media_sorted_by(user_name, principle):
    user_dict = get_name_to_id_dict_from_db()

    user_id = user_dict[user_name]
    all_media = user_media(user_id)
    media_holders_list = list()

    for media in all_media:
        media_holders_list.append(MediaHolder(media))

    sorted_media = sorted(media_holders_list, key=lambda m: m.like_count(), reverse=True)

    total_media_num = len(media_holders_list)
    if total_media_num % 2 == 1:
        mean = sorted_media[total_media_num / 2].like_count()
    else:
        left_mean = sorted_media[total_media_num / 2].like_count()
        right_mean = sorted_media[total_media_num / 2 - 1].like_count()
        mean = 0.5 * (left_mean + right_mean)

    print 'mean   : ', mean
    print 'average: ', sum([m.like_count() for m in media_holders_list]) / float(len(media_holders_list))

    return sorted_media


sorted_by_like = get_media_sorted_by('lav_q', 'like_count')
for p in sorted_by_like:
    print p.link(), p.like_count()



