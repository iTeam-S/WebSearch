#!/usr/bin/env python

from http.client import error
from flask import Flask, redirect, request
from gevent.pywsgi import WSGIServer
from .script import WebSearch

import sys


server = Flask(__name__)


@server.errorhandler(404)
def page_not_found(e):
    return """
        Can't find what you want.
        Please change the query or the extensions
    """


@server.route('/v1/images/<string:query>')
def websearch_image(query):
    limit = request.args.get('limit')
    if limit and limit.isdigit():
        limit = int(limit)
    else:
        limit = 100
    res = None
    try:
        query = query.replace('+', ' ')
        res = WebSearch(query).images
    except error as e:
        print(e)
        return "Error 500, Something Wrong"
    return {res.index(link): link for link in res[:limit]} \
        if res else redirect('/404')


@server.route('/v1/pages/<string:query>')
def websearch_page(query):
    limit = request.args.get('limit')
    if limit and limit.isdigit():
        limit = int(limit)
    else:
        limit = 100
    res = None
    try:
        query = query.replace('+', ' ')
        res = WebSearch(query).pages
    except error as e:
        print(e)
        return "Error 500, Something Wrong"
    return {res.index(link): link for link in res[:limit]} \
        if res else redirect('/404')


@server.route('/v1/<string:ext>/<string:query>')
def websearch(ext, query):
    limit = request.args.get('limit')
    if limit and limit.isdigit():
        limit = int(limit)
    else:
        limit = 100
    try:
        query = query.replace('+', ' ')
        web = WebSearch(query)
        res = web.custom(extension=ext) if ext else web.custom()
    except error as e:
        print(e)
        return "Error 500, Something Wrong"

    return {res.index(link): link for link in res[:limit]} \
        if res and type(res) == list else redirect('/404')


if __name__ == '__main__':
    host = sys.argv[1] if len(sys.argv) == 2 else '0.0.0.0'
    port = int(sys.argv[2]) if len(sys.argv) == 3 else 7888

    print(f'''
 _    _   _____   _____   _____   _____    ___    _____   ____    _   _
| |  | | |  ___| | ___ \ /  ___| |  ___|  / _ \  | ___ \ /  __ \ | | | |
| |  | | | |__   | |_/ / \ `--.  | |__   / /_\ \ | |_/ / | /  \/ | |_| |
| |/\| | |  __|  | ___ \  `--. \ |  __|  |  _  | |    /  | |     |  _  |
\  /\  / | |___  | |_/ / /\__/ / | |___  | | | | | |\ \  | \__/\ | | | |
 \/  \/  \____/  \____/  \____/  \____/  \_| |_/ \_| \_|  \____/ \_| |_/

 Server deployed on {host}:{port}
    ''')  # noqa: W605

    SERVER = WSGIServer((host, port), server)
    SERVER.serve_forever()
