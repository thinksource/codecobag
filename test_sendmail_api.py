""" pytests for Flask """

import pytest
from app import app
import json

@pytest.fixture(scope="module")
def client():
    app.config['TESTING'] = True
    return app.test_client()

@pytest.fixture(scope="module")
def request_context():
    return app.test_request_context('')

def test_session(request_context):
    with request_context:
        # Do something that requires request context
        assert True

def test_email(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    mydict={}
    mydict["to"] = "foretribe@gmail.com"
    mydict["subject"] = "test header"
    mydict["text"] = "test content"
    mydict["cc"] = ""
    mydict["bcc"] = ""
    
    url = '/api/sendmail'
    rs = client.post(url, data=json.dumps(mydict), headers=headers)
    print(rs.data)
    assert 200 == rs.status_code
    assert rs.content_type == mimetype
    rsjson = json.loads(rs.data)
    assert 'message' in rsjson
    assert rsjson['message']=="mails in queue"
    
