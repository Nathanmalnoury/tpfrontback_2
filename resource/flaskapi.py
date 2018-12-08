#!/usr/bin/env python
# -*- coding: latin-1 -*-
import sqlalchemy
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
from flask_sqlalchemy import SQLAlchemy

# TODO : config.py !
app = Flask(__name__)
# api = Api(app)
eng = create_engine('mysql+pymysql://root:root@localhost:3306/exercices')


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
    return jsonify(jsonish)


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
    query = connection.execute("SELECT titre, id FROM article")
    return serialize_get_query(connection, query)


@app.route('/article/<id>')
def get_this_article(id):
    connection = eng.connect()
    query = connection.execute("SELECT * FROM article WHERE id={}".format(id))
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
            "INSERT INTO `article` (`id`, `article`, `titre`) VALUES "
            "(NULL, \"{}\", \"{}\")".format(text(article), text(titre)))

        id = connection.execute(
            "SELECT `id` FROM `article` WHERE article=\"{}\" AND titre=\"{}\"".format(text(article), text(titre))
        ).fetchall()
        connection.close()

        dict_results = {'id': id, 'titre': titre, 'action': 'insert'}
        if len(id) > 1:
            dict_results['warning'] = 'multiple ({}) articles have the same title'.format(len(id))

    except sqlalchemy.exc.ProgrammingError as err:
        return error_json(err)

    return success_json(**dict_results)  # **dictionary access the **kwargs of the function


@app.route('/delete/<id>')
def delete_on_id(id):
    connection = eng.connect()
    query = connection.execute(
        "DELETE FROM `article` WHERE `id` = {}".format(int(str(id))))  # protection contre injection sql ?
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
            "UPDATE `article` SET `article` = \"{}\", `titre` = \"{}\" WHERE `id` = {}"
            .format(text(article), text(titre), id))

    except sqlalchemy.exc.ProgrammingError as err:
        return error_json(err)

    connection.close()
    return success_json(**{'action': 'updated id {}'.format(id)})


@app.route('/about')
def about():
    return 'The about page'


if __name__ == '__main__':
    app.run(debug=True)
