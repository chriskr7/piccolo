#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 SNMP, Inc.

import sys
import requests
import json

from signature import SigGenerator


def print_usage(fname):
    print("Usage: %s [app_id] [json_file]" % fname)
    sys.exit()


def main(argv):

    if len(argv) != 3:
        print_usage(argv[0])

    app_name = argv[1]

    use_api_key = True
    secret_key = "bow_the_snmp"
    app_post = "POST+/v1/app/key"

    url = "http://localhost:7200/v1/app/key"

    if use_api_key:
        api_key = SigGenerator.generate(secret_key, app_post)
        headers = {
            "Piccolo-App-ID": app_name,
            "Piccolo-REST-API-Key": api_key,
            "Content-Type": "application/json"
        }
    else:
        headers = {
            "Piccolo-App-ID": app_name,
            "Content-Type": "application/json"
        }

    try:
        with open(argv[2]) as json_file:
            body = json.load(json_file)
            result = requests.post(url, data=json.dumps(body), headers=headers)
            print(result.text)
    except Exception as e:
        print("Error Occured! : %s", e)

if __name__ == "__main__":
    main(sys.argv)
