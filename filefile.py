from instagram import client, subscriptions
from instagram.client import InstagramAPI
import plotly as py
import plotly.graph_objs as go

myAccessToken  = '723066430.f01b0ca.733da33d9055407fa018ac698908df78'
myClientID     = 'f01b0ca9cbdd43afaabe4abf564e0771'
myClientSecret = 'd45cab5e7d6f4b1581a2b89e9db6c037'

api = InstagramAPI(client_id=myClientID, client_secret=myClientSecret)

NameToId = {
    'sasha': 1069553524,
    'nikita': 15889564,
    'me': 723066430
}


def grab_all_media(userid=NameToId['me']):
    recent_media, getnext = api.user_recent_media(user_id=userid)
    while getnext:
        more_media, getnext = api.user_recent_media(user_id=userid, with_next_url=getnext)
        recent_media.extend(more_media)

    return recent_media


def media_for_graph(userid):
    xs=list()
    ys=list()

    # rec = grab_all_media()
    rec, nxt = api.user_recent_media(user_id=userid)
    for media in rec:
        print media.created_time
        xs.append(media.created_time)
        ys.append(media.like_count)
    ys = list(reversed(ys))
    return xs, ys


xme, yme = media_for_graph(NameToId['me'])
xsh, ysh = media_for_graph(NameToId['sasha'])

trace2 = go.Scatter(
    x=xsh,
    y=ysh,
    mode='lines+markers',
    name="Alexandra",
    hoverinfo='none',
    line=dict(
        shape='spline'
    )
)

trace3 = go.Scatter(
    x=xme,
    y=yme,
    mode='lines+markers',
    name="Andrey",
    hoverinfo='none',
    line=dict(
        shape='spline'
    )
)

py.offline.plot([trace2, trace3])