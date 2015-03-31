#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 FingerApp Studio, Inc.

import sys
import json
import requests

from signature import SigGenerator


def print_usage(fname):
    print("Usage: %s [app_name] [status]" % fname)
    print("\tstatus: run or stop")
    sys.exit()


def main(argv):

    if len(argv) != 3:
        print_usage(argv[0])

    app_name = argv[1]
    status = "__RUN__" if argv[2] == "run" else "__STOP__"

    use_api_key = True
    secret_key = "bow_the_snmp"
    app_put = "PUT+/v1/app"

    url = "http://localhost:7200/v1/app"

    if use_api_key:
        api_key = SigGenerator.generate(secret_key, app_put)
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

    body = {"status": status}

    result = requests.put(url, data=json.dumps(body), headers=headers)

    print(result.text)

if __name__ == "__main__":
    main(sys.argv)
