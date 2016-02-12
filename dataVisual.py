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
    return json_data


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


def stat_by_month(userid, func_y_value):
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
            ys.append(func_y_value(month_likes))
            month = mh.created_time().month
            year = mh.created_time().year
            month_likes = [mh.like_count()]

    return xs, ys


def average_like_by_month(userid):
    def average(month_likes):
        return sum(month_likes)/float(len(month_likes))
    return stat_by_month(userid, average)


def total_like_by_month(userid):
    def total(month_likes):
        return sum(month_likes)
    return stat_by_month(userid, total)


def number_of_media_by_month(userid):
    def number(month_likes):
        return len(month_likes)
    return stat_by_month(userid, number)


dir_html = "html/"
if not os.path.exists(dir_html):
    os.mkdir(dir_html)

plot_files_names = list()

def plot_data_for_users(users, media_getter):
    global plot_files_names
    trace_list = list()
    max_x = 0
    for user in users:
        xme, yme = media_getter(NameToId[user])
        max_x = max([len(xme), max_x])
        trace = go.Scatter(
            x=xme,
            y=yme,
            mode='lines+markers',
            name=user,
            hoverinfo='none',
            line=dict(
                smoothing=0.5,
                shape='spline'
            )
        )
        trace_list.append(trace)

    layout = go.Layout(
        xaxis=dict(
            tickmode="auto",
            nticks=int(1.5 * max_x)
        ),
        yaxis=dict(
            tickmode="auto",
            nticks=12,
            title=media_getter.__name__
        )
    )
    fig = go.Figure(data=trace_list, layout=layout)
    file_name = dir_html + media_getter.__name__ + ".html"
    plot_files_names.append(file_name)
    py.offline.plot(fig, filename=file_name, auto_open=False)


target_users = ['sasha', 'me']

plot_data_for_users(target_users, media_getter=average_like_by_month)
plot_data_for_users(target_users, media_getter=total_like_by_month)
plot_data_for_users(target_users, media_getter=number_of_media_by_month)

str_file_all = dir_html + "all.html"
if os.path.exists(str_file_all):
    os.remove(str_file_all)

result_file = open(str_file_all, 'w+')
result_file.write("<html><head><meta charset=\"utf-8\"/></head>")


def find_between(s, first, last):
    start = s.index(first) + len(first)
    end = s.index(last, start)
    return s[start:end]


for plot_file_name in plot_files_names:
    plot_file = open(plot_file_name, 'r')
    html_data = plot_file.read()
    html_body = find_between(html_data, "<body>", "</body>")
    result_file.write("</br><body>")
    result_file.write(html_body)
    result_file.write("</body>")
    plot_file.close()
    os.remove(plot_file_name)

result_file.write("</html>")

