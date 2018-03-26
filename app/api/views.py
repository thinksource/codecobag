"""
Backend Template

Use this to display server debugging info during development

"""
from flask import render_template
from app.api import api_bp
import requests

import sendgrid
import os
from sendgrid.helpers.mail import *

gridkey="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"
@api_bp.route('/')
def api():
    return render_template('api.html', msg='API Blueprint View')


@api_bp.route('/sendmail', methods=['POST'])
def sendmail():
    url='https://api.mailgun.net/v3/ausingredient.tk/messages'
    content = request.get_json()
    content["from"]="postmaster@ausingredient.tk"
    print(content)
    authurl=HTTPBasicAuth('api','key-e9566dfbfd455918df939ad27239ce16')
    session=requests.Session()
    rs=session.request('post', url, auth=authurl, data=content)
    result=rs.result()
    if (result.status_code<300 and result.status_code>=200):
        return jsonify(result.json())
    else:
        result=sendgrid(content)
        if result.status_code<300 and result.status_code>=200:
            return jsonify(result.json())
        else:
            return jsonify(result.json()), result.status_code
    
def string2emaillist(emailaddress):
    rs=[]
    arr=emailaddress.split(",")
    for i in arr:
        rs.append({"email":i})
    return rs


def sendgrid(content):
    gridkey="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"
    sg = sendgrid.SendGridAPIClient(apikey=gridkey)
    personalization={}
    personalization["to"]=string2emaillist(content["to"])
    personalization["cc"]=string2emaillist(content["cc"])
    personalization["bcc"]=stirng2emaillist(content["bcc"])
    personalization["subject"]=content["subject"]
    data={
        "personalizations": [personalization],
        "from": {
            "email": content["from"]
        },
        "content": [
            {
            "type": "text/plain",
            "value": content["text"]
            }
        ]
        }
    return sg.client.mail.send.post(request_body=data)