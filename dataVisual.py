import os
import sys
import json
import plotly as py
import plotly.graph_objs as go

from datetime import datetime
from mediaHolder import MediaHolder
from usersProvider import name_to_id_dict


def user_media(userid):
    dir_data = 'users/' + str(userid) + '/mediaData.json'
    if not os.path.exists(dir_data):
        return None
    file_data = open(dir_data, 'r')
    json_data = json.load(file_data)
    return json_data


def total_likes_and_media(userid):
    likes=0
    posts=0
    all_media = user_media(userid)
    for media in all_media:
        mh = MediaHolder(media)
        likes += mh.like_count()
        posts += 1

    return likes, posts


def stat_by_month(userid, func_y_value):
    xs = list()
    ys = list()

    all_media = user_media(userid)
    first_media = MediaHolder(all_media[0])
    month = first_media.created_time().month
    year = first_media.created_time().year
    month_likes = [first_media.like_count()]
    del all_media[0]

    def period_switch(m, y, likes):
        xs.append(datetime.strptime(str(m) + '-' + str(y), '%m-%Y'))
        ys.append(func_y_value(likes))
        return mh.created_time().month, mh.created_time().year, [mh.like_count()]

    for media in all_media:
        mh = MediaHolder(media)
        if month == mh.created_time().month:
            month_likes.append(mh.like_count())
        else:
            month, year, month_likes = period_switch(month, year, month_likes)

    period_switch(month, year, month_likes)

    xs.sort()
    ys.reverse()

    return xs, ys


def accumulated_stat_by_month(userid, func_y_value):
    xs, ys = stat_by_month(userid, func_y_value)
    acc_ys = list()
    sm = 0
    for y in ys:
        sm += y
        acc_ys.append(sm)

    return xs, acc_ys


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


def acc_total_like_by_month(userid):
    likes, posts = total_likes_and_media(userid)
    total_average_like = likes / float(posts)
    def total(month_likes):
        return sum(month_likes) / float(total_average_like)
    return accumulated_stat_by_month(userid, total)


def acc_number_of_media_by_month(userid):
    def number(month_likes):
        return len(month_likes)
    return accumulated_stat_by_month(userid, number)


dir_html = "html/"
if not os.path.exists(dir_html):
    os.mkdir(dir_html)

plot_files_names = list()


def trace_for_plot(plot_type):
    if plot_type == 'scatter':
        return go.Scatter(
            mode='lines+markers',
            hoverinfo='none',
            line=dict(
                smoothing=0.5,
                shape='spline'
            )
        )
    if plot_type == 'bar':
        return go.Bar(opacity=0.25)


def plot_data_for_users(users, plot_params_list, plot_title=None):
    global plot_files_names
    trace_list = list()
    max_x = 0
    single_user = len(users) == 1
    for plot_params in plot_params_list:
        media_getter = plot_params[0]
        graph_type = plot_params[1]
        y_title = media_getter.__name__
        for user1 in users:
            g_title = user1
            xme, yme = media_getter(name_to_id_dict()[user1])
            max_x = max([len(xme), max_x])
            trace = trace_for_plot(graph_type)
            trace['x'] = xme
            trace['y'] = yme
            if single_user:
                g_title = media_getter.__name__
                y_title = user1
            trace['name'] = g_title
            trace_list.append(trace)

    layout = go.Layout(
        title=plot_title,
        xaxis=dict(
            tickmode="auto",
            nticks=int(1.5 * max_x)
        ),
        yaxis=dict(
            tickmode="auto",
            nticks=12,
            title=y_title
        ),
        barmode='group'
    )
    fig = go.Figure(data=trace_list, layout=layout)
    file_name = dir_html + graph_type + '_' + media_getter.__name__ + ".html"
    plot_files_names.append(file_name)
    py.offline.plot(fig, filename=file_name, auto_open=False)


target_users = sys.argv[1:]
user_dict = name_to_id_dict()

for user in target_users:
    if user not in user_dict.keys():
        raise ValueError("User not found: " + user)

if len(target_users) == 1:
    plot_data_for_users(target_users, [(average_like_by_month, 'scatter'),
                                       (number_of_media_by_month, 'bar')])
    plot_data_for_users(target_users, [(acc_total_like_by_month, 'scatter'),
                                       (acc_number_of_media_by_month, 'bar')])
else:
    plot_data_for_users(target_users, [(average_like_by_month, 'scatter')])
    plot_data_for_users(target_users, [(number_of_media_by_month, 'bar')])
    plot_data_for_users(target_users, [(acc_number_of_media_by_month, 'bar')])
    plot_data_for_users(target_users, [(total_like_by_month, 'bar')])

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

