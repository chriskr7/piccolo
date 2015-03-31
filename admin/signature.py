# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 FingerApp Studio, Inc.

import hmac
import base64
import hashlib
import json


class SigGenerator:

    @staticmethod
    def generate(secret_key, data):
        if isinstance(secret_key, unicode):
            secret_key = secret_key.encode()
        try:
            json.loads(data)
            return SigGenerator._handle_json(secret_key, data)
        except ValueError:
            if type(data) is dict:
                return SigGenerator._handle_dict(secret_key, data)
            else:
                return SigGenerator._handle_others(secret_key, data)

    @staticmethod
    def _handle_json(secret_key, data):
        fields = SigGenerator._base64_encode(data)
        return SigGenerator._process(secret_key, fields)

    @staticmethod
    def _handle_dict(secret_key, data):
        json_data = json.dumps(data)
        fields = SigGenerator._base64_encode(json_data)
        return SigGenerator._process(secret_key, fields)

    @staticmethod
    def _handle_others(secret_key, data):
        return SigGenerator._process(secret_key, data)

    @staticmethod
    def _process(secret_key, data):
        try:
            sig = SigGenerator._gen_sig(secret_key, data)
            sig = SigGenerator._base64_encode(sig).decode()
            return sig
        except:
            raise

    @staticmethod
    def _gen_sig(secret_key, data):
        try:
            sig = hmac.new(secret_key, msg=data, digestmod=hashlib.sha256).digest()
            return sig
        except:
            raise

    @staticmethod
    def _base64_encode(data):
        return base64.b64encode(data, altchars='-_')
