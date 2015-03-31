#!/usr//bin/env python

import json
import requests

url = "http://localhost:7200/v1/app/push"

headers = {
    "Piccolo-App-ID": "bulma",
    "Content-Type": "application/json"
}


a_content = {
    "seq": 1,
    "alert_type": "02",
    "alert_sub_type": "00",
    "title": "Chris",
    "msg": "Chris is Cute :)"
}

i_content = {
    "seq": 1,
    "alert_type": "01",
    "alert_sub_type": "00"
}


send_content = json.dumps(a_content)

body = {
    "recv_id_list": ["test05"],
    "badge_cnt_list": [1],
    "show_msg": "Chris says MeRong",
    "msg": {
                "type": "news_msg",
                "content": send_content
    }
}

r = requests.post(url, data=json.dumps(body), headers=headers)
print r.text
