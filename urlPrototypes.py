from string import replace

recentMediaUrlPrototype = \
    "https://api.instagram.com/v1/users/{user-id}/media/recent/?access_token=ACCESS-TOKEN"
userUrlPrototype = \
    "https://api.instagram.com/v1/users/{user-id}/?access_token=ACCESS-TOKEN"
selfInfo = \
    "https://api.instagram.com/v1/users/self/?access_token=ACCESS-TOKEN"
selfFollowedBy = \
    "https://api.instagram.com/v1/users/self/followed-by?access_token=ACCESS-TOKEN"
selfFollows = \
    "https://api.instagram.com/v1/users/self/follows?access_token=ACCESS-TOKEN"
selfRelationshipToUser = \
    "https://api.instagram.com/v1/users/{user-id}/relationship?access_token=ACCESS-TOKEN"


def get_url(user_id, access_token, prototype):
    tmp = replace(prototype, '{user-id}', str(user_id))
    return replace(tmp, "ACCESS-TOKEN", access_token)

