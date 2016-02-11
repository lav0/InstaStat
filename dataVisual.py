import os
import json
import plotly as py
import plotly.graph_objs as go

from datetime import datetime
from updateData import NameToId
from mediaHolder import MediaHolder


def user_media(userid):
    dir_data = str(userid) + '/mediaData.json'
    if not os.path.exists(dir_data):
        return None
    file_data = open(dir_data, 'r')
    json_data = json.load(file_data)
    return json_data #['data']


def all_media_for_graph(userid):
    xs = list()
    ys = list()

    # rec = grab_all_media()
    rec = user_media(userid)
    for med in rec:
        media_holder = MediaHolder(med)
        created_time = media_holder.created_time()
        like_count = media_holder.like_count()
        print created_time, like_count
        xs.append(created_time)
        ys.append(like_count)

    return xs, ys


def media_for_graph_by_month(userid):
    xs = list()
    ys = list()

    all_media = user_media(userid)
    first_media = MediaHolder(all_media[0])
    month = first_media.created_time().month
    year = first_media.created_time().year
    month_likes = [first_media.like_count()]
    del all_media[0]
    for media in all_media:
        mh = MediaHolder(media)
        if month == mh.created_time().month:
            month_likes.append(mh.like_count())
        else:
            xs.append(datetime.strptime(str(month) + '-' + str(year), '%m-%Y'))
            ys.append(sum(month_likes)/float(len(month_likes)))
            month = mh.created_time().month
            year = mh.created_time().year
            month_likes = [mh.like_count()]

    return xs, ys


layout = go.Layout(
    xaxis=dict(
        autorange=True, showgrid=True, zeroline=False, autotick=True
    ),
    yaxis=dict(
        autorange=True, showgrid=True, zeroline=True, autotick=True
    )
)


def plot_data_for_users(users, media_getter):
    trace_list = list()
    for user in users:
        xme, yme = media_getter(NameToId[user])

        trace = go.Scatter(
            x=xme,
            y=yme,
            mode='lines+markers',
            name=user,
            hoverinfo='none',
            line=dict(
                shape='spline'
            )
        )
        trace_list.append(trace)

    fig = go.Figure(data=trace_list, layout=layout)
    py.offline.plot(fig)

plot_data_for_users(['sasha', 'me'], media_getter=media_for_graph_by_month)
