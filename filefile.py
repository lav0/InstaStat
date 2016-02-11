from instagram import client, subscriptions
from instagram.client import InstagramAPI
import plotly as py
import plotly.graph_objs as go
from updateData import NameToId
from updateData import DataUpdater
from updateData import myAccessToken
from updateData import myClientID
from updateData import myClientSecret
import os
import json


api = 0


def setup_api():
    global api
    api = InstagramAPI(client_id=myClientID, client_secret=myClientSecret)



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
    #json.dumps(rec.data())
    for media in rec:
        print media.created_time, media.like_count
        xs.append(media.created_time)
        ys.append(media.like_count)

    return xs, ys


def plot_my_first_stat():
    xme, yme = media_for_graph(NameToId['me'])

    print ' '
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


def expand_data(data):
    if isinstance(data, dict):
        for key in data.keys():
            print " {", key, ":",  expand_data(data[key]), "} "
    elif isinstance(data, list):
        for item in data:
            print " [", expand_data(item), "] "

    return data


DataUpdater(NameToId['nikita'], myAccessToken).update_media_data()

# data_file = 0
# path = str(NameToId['me'])
# if os.path.exists(path):
#     data_file = open(path + '/userData.json')
# json_data = json.load(data_file)
# print expand_data(json_data)

# setup_api()
# plot_all_data_for_users()