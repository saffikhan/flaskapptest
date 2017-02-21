from flask import Flask, jsonify, request, make_response
import xconfig

app = Flask(__name__)

hints = {}
for i in range(xconfig.SAMPLE_DATA_MAX):
    hints[i] = {
        'hint': 'http:/resource/{0!s}'.format(i),
    }


@app.route('/stats', methods=['GET'])
def test():
    return jsonify({'message' : 'It works!'})

@app.route('/statsa', methods = ['GET'])
def api_hello():
    data = {
        'number' : 3
    }
    js = json.dumps(data)

    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://luisrei.com'

    return resp


@app.route('/', methods=['POST'])
def testPost():
    if request.json:
        # As if it had taken by id
        hint = hints[request.json['userCode']]
        hint['status'] = True

        return jsonify(hint)

    return jsonify({'status': False, "message": "Invalid data!"})


if __name__ == '__main__':
    app.run(debug=True,
            host="0.0.0.0",
            port=xconfig.EXTERNAL_SERVER_PORT)
