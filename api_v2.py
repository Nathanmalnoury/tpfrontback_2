#!/usr/bin/env python3
# -*- coding: latin-1 -*-

import sqlalchemy
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
import resources.config as cfg
import resources.functions as f
import resources.utils as u

app = Flask(__name__)
eng = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(cfg.mysql['user'],
                                                            cfg.mysql['passwd'],
                                                            cfg.mysql['host'],
                                                            cfg.mysql['port'],
                                                            cfg.mysql['db']))


# should be accessed by '/article/titre'
@app.route('/article', methods=['GET', 'POST', 'PUT', 'DELETE'])
def main():
    if request.method == 'GET':
        dict_request = u.url_parser(request.full_path)
        if not dict_request or 'id' not in dict_request.keys():
            try:
                return f.get_all_article(eng, cfg)
            except sqlalchemy.exc.ProgrammingError as err:
                return u.error_json(err)

        else:
            try:
                return f.get_this_article(eng, cfg, dict_request['id'])
            except sqlalchemy.exc.ProgrammingError as err:
                return u.error_json(err)

    elif request.method == 'POST':
        post_json = request.get_json()
        if not post_json:
            return u.error_json(custom="no json was received")
        return f.add_article(eng, cfg, post_json)

    elif request.method == 'PUT':
        post_json = request.get_json()
        if not post_json:
            return u.error_json(custom="no json was received")
        return f.update_on_id(eng, cfg, post_json)

    elif request.method == "DELETE":  # method == 'DELETE'
        post_json = request.get_json()
        if not post_json:
            return u.error_json(custom="no json was received")
        else:
            return f.delete_on_id(eng, cfg, post_json)

    else:
        return u.error_json("this method is not implemented : {}".format(request.method))


if __name__ == '__main__':
    app.run(debug=True)
