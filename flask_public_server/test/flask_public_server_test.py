import os,sys
import json
from ..flask_public_server import flask_public_server
import unittest

time_spent = 30
code = '21'

def post(app, code, time_spent):
    request_data = dict()
    if code != None:
        request_data['code'] = code
    if time_spent != None:
        request_data['time_spen'] = time_spent
    return app.post('/site', data=json.dumps(request_data), content_type='application/json')


class PublicServerTestCase(unittest.TestCase):

    def setUp(self):
        sys._called_from_test = True
        self.app = flask_public_server.app.test_client()

    def test_incorrect_parameter(self):
        response = post(self.app, code, time_spent)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_data['message'], 'Invalid data!')
        self.assertEqual(json_data['status'], False)

if __name__ == '__main__':
    unittest.main()