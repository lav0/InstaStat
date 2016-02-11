import json
from pprint import pprint

#
# class Payload(object):
#     def __init__(self, j):
#         self.__dict__ = json.loads(j)

# file = open('_data.json')
# data = json.load(file)
#
# #print data['caption']['created_time']
# #print [type(d) for d in data['data']]
#
# print "Total count: ", len(data['data'])
# for d in data['data']:
#     print d['likes']['count'], d['link']
#     # for key in likes.keys():
#     #     print type(likes[key])
#     # for key in d.keys():
#     #     print key, type(d[key])
#
# new_data = open('_newdata.json', 'w')
# json.dump(data, new_data)

d = [ {'one': 1, 'two': 2} ]
d1 = {'ou': 0, 'tu': 00}
d.append(d1)
f = open("__testAppend.json", 'w+')
json.dump(d, f)
