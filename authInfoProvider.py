import json
import os


def get_auth_token(token):
    dir_data = "data/auth.json"
    if not os.path.exists(dir_data):
        raise ValueError(token + " is not provided. Put in 'data/auth.json' !")
    auth_file = open(dir_data, 'r')
    data = json.load(auth_file)
    value = str(data[token])
    if not isinstance(data, dict):
        raise ValueError(token + " is not provided. Put in 'data/auth.json' !!")
    return value


def get_access_token():
    return get_auth_token(u'AccessToken')


def get_client_id():
    return get_auth_token("ClientID")


def get_client_secret():
    return get_auth_token("ClientSecret")

