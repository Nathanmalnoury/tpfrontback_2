#!/usr/bin/env python
# -*- coding: latin-1 -*-

import sqlalchemy
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text

import config as cfg

app = Flask(__name__)
eng = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(cfg.mysql['user'],
                                                            cfg.mysql['passwd'],
                                                            cfg.mysql['host'],
                                                            cfg.mysql['port'],
                                                            cfg.mysql['db']))


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


@app.route('/allTitles/')
def get_all_artitle():
    connection = eng.connect()
    query = connection.execute(
        "SELECT {}, {} FROM {}".format(cfg.mysql['title'], cfg.mysql['id'], cfg.mysql['article_table']))
    return serialize_get_query(connection, query)


@app.route('/article/<id>')
def get_this_article(id):
    connection = eng.connect()
    query = connection.execute(
        "SELECT * FROM {} WHERE {}={}".format(cfg.mysql['article_table'], cfg.mysql['id'], id))
    return serialize_get_query(connection, query)


@app.route('/addNewArticle/', methods=['POST'])
def add_article():
    # TODO parser, envoyer ça dans la ddb
    post_json = request.get_json()
    if u'titre' not in post_json.keys():
        return error_json('empty title (must be called \'titre\')')

    connection = eng.connect()
    try:
        if 'article' in post_json.keys():
            article = post_json[u'article']
        else:
            article = u'Ecrivez ici'

        titre = post_json[u'titre']
        query = connection.execute(
            "INSERT INTO `{}` (`{}`, `{}`, `{}`) VALUES "
            "(NULL, \"{}\", \"{}\")".format(cfg.mysql['article_table'],
                                            cfg.mysql['id'],
                                            cfg.mysql['article'],
                                            cfg.mysql['title'],
                                            text(article),
                                            text(titre)))

        id = connection.execute(
            "SELECT `{}` FROM `{}` WHERE {}=\"{}\" AND {}=\"{}\"".format(
                cfg.mysql['id'],
                cfg.mysql['article_table'],
                cfg.mysql['article'],
                text(article),
                cfg.mysql['title'],
                text(titre))
        ).fetchall()
        connection.close()

        dict_results = {'id': cfg.mysql['id'], 'titre': cfg.mysql['title'], 'action': 'add new'}
        if len(id) > 1:
            dict_results['warning'] = "multiple ({}) articles have the same title".format(len(id))

    except sqlalchemy.exc.ProgrammingError as err:
        return error_json(err)

    return success_json(**dict_results)  # **dictionary access the **kwargs of the function


@app.route('/delete/', methods=['POST'])
def delete_on_id():
    post_json = request.get_json()
    if 'id' not in post_json.keys():
        return error_json(u'id is missing')
    if type(post_json['id']) != int:  # anti injection
        return error_json((u'id not an int'))
    connection = eng.connect()
    query = connection.execute(
        "DELETE FROM `{}` WHERE `{}` = {}".format(
            cfg.mysql['article_table'],
            cfg.mysql['id'],
            post_json['id']))  # protection contre injection sql ?
    return success_json(**{"action": "delete"})


@app.route('/update/', methods=['POST'])
def update_on_id():
    post_json = request.get_json()
    if 'id' not in post_json.keys():
        return error_json(u'id is missing')
    connection = eng.connect()
    id = post_json['id']
    if type(id) != int:
        error_json("id is not an integer")

    article = post_json[u'article']
    titre = post_json[u'titre']
    try:
        query = connection.execute(
            "UPDATE `{}` SET `{}` = \"{}\", `{}` = \"{}\" WHERE `id` = {}"
                .format(
                cfg.mysql['article_table'],
                cfg.mysql['article'],
                text(article),
                cfg.mysql['title'],
                text(titre),
                cfg.mysql['id'],
                id))

    except sqlalchemy.exc.ProgrammingError as err:
        return error_json(err)

    connection.close()
    return success_json(**{'action': 'updated id {}'.format(id)})


@app.route('/about')
def about():
    return 'The about page'


if __name__ == '__main__':
    app.run(debug=True)
