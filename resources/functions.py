#!/usr/bin/env python3
# -*- coding: latin-1 -*-

import sqlalchemy
from flask import jsonify, request
from sqlalchemy import create_engine, text
from resources.utils import serialize_get_query, error_json, success_json

def get_all_article(eng, cfg):
    connection = eng.connect()
    query = connection.execute(
        "SELECT {}, {} FROM {}".format(cfg.mysql['title'], cfg.mysql['id'], cfg.mysql['article_table']))
    return serialize_get_query(connection, query)


def get_this_article(eng, cfg, id):
    connection = eng.connect()
    query = connection.execute(
        "SELECT * FROM {} WHERE {}={}".format(cfg.mysql['article_table'], cfg.mysql['id'], id))
    return serialize_get_query(connection, query)


def add_article(eng, cfg, post_json):
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

        id_ = connection.execute(
            "SELECT `{}` FROM `{}` WHERE {}=\"{}\" AND {}=\"{}\"".format(
                cfg.mysql['id'],
                cfg.mysql['article_table'],
                cfg.mysql['article'],
                text(article),
                cfg.mysql['title'],
                text(titre))
        ).fetchall()
        connection.close()

        id = [r.values()[0] for r in id_]
        dict_results = {'id': max(id), 'titre': titre, 'action': 'add new'}
        if len(id) > 1:
            dict_results['warning'] = "multiple ({}) articles have the same title : {}".format(len(id), id)

    except sqlalchemy.exc.ProgrammingError as err:
        return error_json(err)

    return success_json(**dict_results)  # **dictionary access the **kwargs of the function


def delete_on_id(eng, cfg, post_json):
    if 'id' not in post_json.keys():
        return u.error_json(u'id is missing')

    def delete_one_id(eng, cfg, id):
        connection = eng.connect()
        query = connection.execute(
            "DELETE FROM `{}` WHERE `{}` = {}".format(
                cfg.mysql['article_table'],
                cfg.mysql['id'],
                int(id)))  # protection contre injection sql ?

    if type(post_json['id']) == list:
        for id in post_json['id']:
            delete_one_id(eng, cfg, id)
        return success_json(**{"action": "multiple delete"})


    elif type(post_json['id']) == int:
        delete_one_id(eng, cfg, post_json['id'])
        return success_json(**{"action": "delete"})
    else:
        return error_json("unsupported format for id : {}".format(post_json['id']))


def update_on_id(eng, cfg, post_json):
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
            "UPDATE `{}` SET `{}` = \"{}\", `{}` = \"{}\" WHERE `{}` = {}"
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
