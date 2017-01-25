from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

@app.route('/', methods=['GET'])
def testGet():
    return jsonify({'hint' : 'This is an example hint for GET testing purposes 123abc'})

@app.route('/', methods=['POST'])
def testPost():
    return jsonify({'hint' : 'This is an example hint for POST testing purposes 123abc'})

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0',port=5000)