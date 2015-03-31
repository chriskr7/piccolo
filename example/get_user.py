#!/usr/bin/env python

import json
import requests

from signature import SigGenerator

url = "http://localhost:8300/v1/app/user"


use_api_key = False
secret_key = "bow_the_snmp"
app_post = "GET+/1/app/user"

if use_api_key:
    api_key = SigGenerator.generate(secret_key, app_post)
    headers = {
        "Piccolo-App-ID": "snek",
        "Piccolo-REST-API-Key": api_key,
        "Content-Type": "application/json"
    }
else:
    headers = {
        "Piccolo-App-ID": "snek",
        "Content-Type": "application/json"
    }

body = {
    "uid": "chriskr7@gmail.com"
}

result = requests.get(url, data=json.dumps(body), headers=headers)

print(result.text)
