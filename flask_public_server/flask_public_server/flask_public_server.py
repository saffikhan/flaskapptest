import httplib
import logging.handlers
import os,copy, sys
import socket
import json

from flask import Flask, request, make_response, jsonify

import requests, requests.exceptions

import xconfig

app = Flask(__name__)

DIR = os.path.dirname(os.path.abspath(__file__))

# log setup
app.logger.setLevel(logging.DEBUG)

log_dir = os.path.join(DIR, 'logs')
if not os.path.exists(log_dir):
    os.mkdir(log_dir)
handler = logging.handlers.RotatingFileHandler(
    os.path.join(log_dir, 'site.log'),
    maxBytes=1024 ** 2,
    backupCount=3)
app.logger.addHandler(handler)

def get_instrcutor_id(token):
    if token == '':
        return 0
    return 1

# aux
POST = 'POST'

def jerror(msg=u"Invalid data!", code=400):
    """Generic error"""
    response = make_response(jsonify({"status": False, "message": msg}), code)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/stats', methods=['GET'])
def site_get():
    token = 'dhjkadlalddajdajksdhkad'
    instructor_id = get_instrcutor_id(token)
    if instructor_id:
        res = requests.get('%s/%d' % (xconfig.EXTERNAL_SERVER_URL_STATS_ANALYSIS, instructor_id))

        if res.status_code != 200:
            return jsonify(res.text), res.status_code

        # Reads data from external server
        jdata = res.text

        # Prepare the return response.
        response = make_response(jdata, 200)

        # Uses the server header
        ctype = res.headers.get('content-type')

        if ctype is not None:
            response.headers['content-type'] = ctype
            app.logger.info('server content-type: {0:s}'.format(ctype))

        return jsonify(res.text)

    return 401


@app.route('/site', methods=['POST'])
def site_view():
    """Data posted to this view is in json format."""
    app.logger.info("received [{0.path}] {0.data}".format(request))
    
    new_request = json.loads(request.data)

    # hard coded values for now to match hints_provider input
    new_request['student_id'] = 1
    new_request['exercise_id'] = 101

    print json.dumps(new_request)

    # I could do more checks here
    if request.json:
        if hasattr(sys, '_called_from_test'):
            if 'code' not in request.data or 'time_spent' not in request.data:
                return jerror()

            return jsonify(json.dumps(new_request)), 200

        else:
            try:
                res = requests.post(xconfig.EXTERNAL_SERVER_URL,
                                    data=json.dumps(new_request),
                                    headers={
                                        'Content-Type': 'application/json'
                                    })
            except requests.exceptions.RequestException as err:
                msg = str(err)
                try:
                    msg = msg.decode('utf8')
                except UnicodeDecodeError:
                    msg = msg.decode('Windows-1252')
                return jerror(msg=msg, code=500)

            # It could do some processing on the data, but it just returns it to the client

            # Did something go wrong on the server?
            if res.status_code != 200:
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
    testing = False
    app.run(host="0.0.0.0",
            port=xconfig.SITE_SERVER_PORT,
            debug=True)
