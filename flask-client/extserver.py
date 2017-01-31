from flask import Flask, jsonify, request, make_response
import xconfig

app = Flask(__name__)

hints = {}
for i in range(xconfig.SAMPLE_DATA_MAX):
    hints[i] = {
        'hint': 'http:/resource/{0!s}'.format(i),
    }


@app.route('/', methods=['GET'])
def testGet():
    return jsonify({'hint': 'This is an example hint for GET testing purposes 123abc'})


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
