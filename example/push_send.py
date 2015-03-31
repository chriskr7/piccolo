#!/usr/bin/env python

import json
import requests

from signature import SigGenerator

url = "http://localhost:8300/v1/app/push"


use_api_key = True
secret_key = "bow_the_snmp"
app_post = "POST+/1/app/push"

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

#
#  Note that these contents can be any format once client(iphone, android) and sever-side settled
#

# android
a_content = {
    "seq": 1,
    "alert_type": "01",
    "alert_sub_type": "00",
    "title": "Chris",
    "msg": "Chris is Cute :)"
}

# i-phone
i_content = {
    "seq": 1,
    "alert_type": "01",
    "alert_sub_type": "00"
}

#
# body
#   - recv_id_list & badge_cnt_list order should correspond each other.
#   - the element of badge_cnt_list should be exsting_count + new_count.
#

send_content = json.dumps(a_content)

body = {
    "recv_id_list": ["chriskr7@gmail.com"],
    "badge_cnt_list": [1],
    "show_msg": "Chris says MeRong",
    "msg": {
        "type": "news_msg",
        "content": send_content
    }
}

result = requests.post(url, data=json.dumps(body), headers=headers)

print(result.text)
