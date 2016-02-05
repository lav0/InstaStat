import json


class Payload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

file = open('_data.json')
data = file.read()
j = '{"action": "print", "method": "onData", "data": "Madan Mohan"}'
p = Payload(j)

print p.action
print p.data