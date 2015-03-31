#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 FingerApp Studio, Inc.

import sys
import requests
from signature import SigGenerator


def print_usage(fname):
    print("Usage: %s [app_name]" % fname)
    sys.exit()


def main(argv):

    if len(argv) != 2:
        print_usage(argv[0])

    app_name = argv[1]

    use_api_key = True
    secret_key = "bow_the_snmp"
    app_post = "DELETE+/v1/app"

    url = "http://localhost:7200/v1/app"

    if use_api_key:
        api_key = SigGenerator.generate(secret_key, app_post)
        headers = {
            "Piccolo-App-ID": app_name,
            "Piccolo-REST-API-Key": api_key
        }
    else:
        headers = {
            "Piccolo-App-ID": app_name
        }

    result = requests.delete(url, headers=headers)

    print(result.text)

if __name__ == "__main__":
    main(sys.argv)
