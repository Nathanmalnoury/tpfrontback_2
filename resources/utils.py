#!/usr/bin/env python3
# -*- coding: latin-1 -*-
from flask import jsonify


def url_parser(url):
    split_index = url.find('?')  # returns first index of '?', in case there are ? in the body
    url = url[split_index + 1:]
    if url :
            dict_response = {}
            for chunk in url.split('&'):
                [key, value] = chunk.split('=')
                print(key, value)
                dict_response[str(key)] = value
            return dict_response
    else:
        return {}


def serialize_get_query(connection, query):
    jsonish = dict()
    jsonish["success"] = True
    jsonish["result"] = []
    try:
        for t in query.fetchall():  # returns a tuple
            tmp_dict = {}
            for index, key in enumerate(query.keys()):
                tmp_dict[key] = t[index]
            jsonish["result"].append(tmp_dict)
        connection = connection.close()
        return jsonify(jsonish)

    except:
        return error_json()


def error_json(custom=None):
    jsonish = dict()
    jsonish["success"] = False
    jsonish["result"] = []
    if custom:
        jsonish["result"] = str(custom)
    return (jsonish)


def success_json(**kwargs):
    # kwargs let us pass custom dictionary to pass into the return json
    jsonish = {}
    jsonish["success"] = True
    jsonish["result"] = []
    if kwargs:
        jsonish["result"].append(kwargs)
    return jsonify(jsonish)
