import httplib
import logging.handlers
import os
import socket

from flask import Flask, request, make_response, jsonify
import requests

import xconfig

app = Flask(__name__)

DIR = os.path.dirname(os.path.abspath(__file__))

# log setup
app.logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(
    os.path.join(DIR, 'logs', 'site.log'),
    maxBytes=1024 ** 2,  # 1M
    backupCount=3)
app.logger.addHandler(handler)

# aux
POST = 'POST'


def jerror(msg=u"Invalid data!", code=200):
    """Generic error"""
    response = make_response(jsonify({"status": False, "message": msg}), code)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/site', methods=['POST'])
def site_view():
    """Data posted to this view is in json format."""
    app.logger.info("received [{0.path}] {0.data}".format(request))

    if request.json:
        try:
            res = requests.post(
                "http://{0.EXTERNAL_SERVER_HOST}:{0.EXTERNAL_SERVER_PORT}".format(xconfig),
                data=request.data,
                headers={
                    'Content-Type': 'application/json'
                })
        except (httplib.error, socket.error) as err:
            msg = str(err)
            try:
                msg = msg.decode('utf8')
            except UnicodeDecodeError:
                msg = msg.decode('Windows-1252')
            return jerror(msg=msg, code=500)

        # It could do some processing on the data, but it just returns it to the client

        # Did something go wrong on the server?
        if res.status != 200:
            return jerror()

        # Reads data from external server
        jdata = res.text

        # Prepare the return response.
        response = make_response(jdata, 200)

        # Uses the server header
        ctype = res.headers.get('content-type')

        if ctype is not None:
            response.headers['content-type'] = ctype
            app.logger.info('server content-type: {0:s}'.format(ctype))

        return response

    return jerror()


if __name__ == '__main__':
    app.run(host="0.0.0.0",
            port=xconfig.SITE_SERVER_PORT,
            debug=True)
