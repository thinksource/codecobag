"""
Backend Template

Use this to display server debugging info during development

"""
from flask import render_template,request,jsonify
from app.api import api_bp
import requests
from requests.auth import HTTPBasicAuth
import json

from sendgrid.helpers.mail import *
from collections import namedtuple
import sendgrid
gridkey="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"

def string2emaillist(emailaddress):
    rs=[]
    arr=emailaddress.split(",")
    for i in arr:
        rs.append({"email":i.strip()})
    return rs


def sendmail_grid(content):
    gridkey = "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"
    sg = sendgrid.SendGridAPIClient(apikey=gridkey)
    personalization={}
    if 'to' in content:
        personalization["to"]=string2emaillist(content["to"])
    if 'cc' in content:
        personalization["cc"]=string2emaillist(content["cc"])
    if 'bcc' in content:
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

@api_bp.route('/')
def api():
    return render_template('api.html', msg='API Blueprint View')


@api_bp.route('/sendmail', methods=['GET', 'POST'])
def sendmail():
    url='https://api.mailgun.net/v3/ausingredient.tk/messages'
    content = request.get_json()
    content["from"]="postmaster@ausingredient.tk"
    if(content["cc"]==""):
        del content["cc"]
    
    if(content["bcc"]==""):
        del content["bcc"]
    
    if(content["to"]==""):
        del content["to"]
    
    # print(content)
    authurl=HTTPBasicAuth('api','key-e9566dfbfd455918df939ad27239ce16')
    session=requests.Session()
    rs=session.request('post', url, auth=authurl, data=content)
    # print(dir(rs.text))
    # r={'status_code':400, 'text':"error"}
    # rs=namedtuple('Struct', r.keys())(*r.values())
    result=json.loads(rs.text)
    # result=rs
    if (rs.status_code<300 and rs.status_code>=200):
        return jsonify(result)
    else:
        result=sendmail_grid(content)
        print(result.body)
        if(result.status_code<300 and result.status_code>=200):
            if (len(result.body)>0):
                return jsonify(json.loads(result.body))
            else:
                return jsonify(message="mails in queue")
        else:
            return jsonify(json.loads(r)), rs.status_code
