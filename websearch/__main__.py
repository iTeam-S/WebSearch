#!/usr/bin/env python

from http.client import error
from flask import Flask, redirect
from gevent.pywsgi import WSGIServer
from .script import WebSearch

import sys


APP = Flask(__name__)

@APP.errorhandler(404)
def page_not_found(e):
    return """                                                  
        Can't find what you want. 
        Please change the query or the extensions                  
    """
    
@APP.route('/v1/image/<string:query>')
def websearch_image(query):
    res = None
    try:
        query = query.replace('+', ' ')
        res = WebSearch(query).images
    except error as e:
        print(e)
        return "Error 500, Something Wrong"
    return {res.index(link):link for link in res} if res else redirect('/404')


@APP.route('/v1/page/<string:query>')
def websearch_page(query):
    res = None
    try:
        query = query.replace('+', ' ')
        res = WebSearch(query).pages
    except error as e:
        print(e)
        return "Error 500, Something Wrong"
    return {res.index(link):link for link in res} if res else redirect('/404')

@APP.route('/v1/custom/<string:query>')
def websearch(query):
    res = None
    try:
        ext = None
        q = query.replace('+', ' ')
        if '~' in q:
            ext, q = q[q.rfind('~')+1:], q[:q.rfind('~')]
        web = WebSearch(q)
        res = web.custom(extension=ext) if ext else web.custom()
    except error as e:
        print(e)
        return "Error 500, Something Wrong"

    return {res.index(link):link for link in res} if res and type(res) == list else redirect('/404')


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
    ''')

    SERVER = WSGIServer((host,port),APP)
    SERVER.serve_forever()
