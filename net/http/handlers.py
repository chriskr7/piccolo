# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 FingerApp Studio, Inc.

import tornado.gen
import tornado.web
import tornado.escape
import tornado.httpserver

from boto.sqs import jsonmessage


class MainHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):
        self.write("Welcome to SNMP Push API Page :P")
        self.finish()


class BaseHandler(tornado.web.RequestHandler):

    def _parse_json(self):
        content_type = self.request.headers.get("Content-Type", "")
        if content_type.startswith("application/json"):
            try:
                self.arguments = tornado.escape.json_decode(self.request.body)
            except ValueError:
                raise tornado.httpserver._BadRequestException(
                    "Invalid JSON structure")
            if type(self.arguments) != dict:
                raise tornado.httpserver._BadRequestException(
                    "Not Key-Value type")
        return self.arguments

    def _get_app_id(self):
        return self.request.headers.get("Piccolo-App-ID")

    def _get_api_key(self):
        return self.request.headers.get("Piccolo-REST-API-Key")

    def _check_api_key(self, a, b):
        if (a != b):
            raise tornado.web.HTTPError(401)

    def _write_error(self, status_code):
        self.set_status(status_code)
        self.write_error(status_code=status_code)

    @property
    def db(self):
        return self.application.db


class AppHandler(BaseHandler):

    @tornado.web.asynchronous
    def delete(self):
        if self.db.config.application.use_api_key:
            self._check_api_key(self.db.config.apikey.app.delete,  self._get_api_key())
        app_id = self._get_app_id()
        result = self.db.delete_app(app_id)
        if result is not None:
            self.write(tornado.escape.json_encode(result))
            self.finish()
        else:
            self._write_error(status_code=404)

    @tornado.web.asynchronous
    def post(self):
        if self.db.config.application.use_api_key:
            self._check_api_key(self.db.config.apikey.app.post,  self._get_api_key())
        app_id = self._get_app_id()
        result = self.db.insert_app(app_id)
        if result is not None:
            self.write(tornado.escape.json_encode(result))
            self.finish()
        else:
            self._write_error(status_code=501)

    @tornado.web.asynchronous
    def put(self):
        if self.db.config.application.use_api_key:
            self._check_api_key(self.db.config.apikey.app.put,  self._get_api_key())
        app_id = self._get_app_id()
        body = self._parse_json()
        result = self.db.update_app(app_id, body["status"])
        if result is not None:
            self.write(tornado.escape.json_encode(result))
            self.finish()
        else:
            self._write_error(status_code=501)

    @tornado.web.asynchronous
    def get(self):
        if self.db.config.application.use_api_key:
            self._check_api_key(self.db.config.apikey.app.get,  self._get_api_key())
        app_id = self._get_app_id()
        result = self.db.select_app(app_id)
        if result is not None:
            self.write(tornado.escape.json_encode(result))
            self.finish()
        else:
            self._write_error(status_code=404)


class UserHandler(BaseHandler):

    @tornado.web.asynchronous
    def post(self):
        if self.db.config.application.use_api_key:
            self._check_api_key(self.db.config.apikey.user.post,  self._get_api_key())
        app_id = self._get_app_id()
        body = self._parse_json()
        result = self.db.insert_user(app_id, body["uid"], body["dev_token"], body["os_type"])
        if result is not None:
            self.write(tornado.escape.json_encode(result))
            self.finish()
        else:
            self._write_error(status_code=501)

    @tornado.web.asynchronous
    def get(self):
        if self.db.config.application.use_api_key:
            self._check_api_key(self.db.config.apikey.user.get,  self._get_api_key())
        app_id = self._get_app_id()
        body = self._parse_json()
        result = self.db.select_user(app_id, body["uid"])
        if result is not None:
            self.write(tornado.escape.json_encode(result))
            self.finish()
        else:
            self._write_error(status_code=404)

    @tornado.web.asynchronous
    def put(self):
        if self.db.config.application.use_api_key:
            self._check_api_key(self.db.config.apikey.user.put,  self._get_api_key())
        app_id = self._get_app_id()
        body = self._parse_json()
        result = self.db.update_user(
            app_id, body["uid"], body["dev_token"], body["os_type"])
        if result is not None:
            self.write(tornado.escape.json_encode(result))
            self.finish()
        else:
            self._write_error(status_code=501)

    @tornado.web.asynchronous
    def delete(self):
        if self.db.config.application.use_api_key:
            self._check_api_key(self.db.config.apikey.user.delete,  self._get_api_key())
        app_id = self._get_app_id()
        body = self._parse_json()
        result = self.db.delete_user(app_id, body["uid"])
        if result is not None:
            self.write(tornado.escape.json_encode(result))
            self.finish()
        else:
            self._write_error(status_code=404)


class KeyHandler(BaseHandler):

    @tornado.web.asynchronous
    def post(self):
        if self.db.config.application.use_api_key:
            self._check_api_key(self.db.config.apikey.key.post,  self._get_api_key())
        app_id = self._get_app_id()
        body = self._parse_json()
        result = self.db.insert_key(
            app_id, body["gcm_key"], body["ios_key"], body["ios_cert"])
        if result is not None:
            self.write(tornado.escape.json_encode(result))
            self.finish()
        else:
            self._write_error(status_code=501)

    @tornado.web.asynchronous
    def delete(self):
        if self.db.config.application.use_api_key:
            self._check_api_key(self.db.config.apikey.key.delete,  self._get_api_key())
        app_id = self._get_app_id()
        result = self.db.delete_key(app_id)
        if result is not None:
            self.write(tornado.escape.json_encode(result))
            self.finish()
        else:
            self._write_error(status_code=404)


class PushHandler(BaseHandler):

    @tornado.web.asynchronous
    def post(self):
        if self.db.config.application.use_api_key:
            self._check_api_key(self.db.config.apikey.push,  self._get_api_key())

        # check app's running status
        app_id = self._get_app_id()

        if self.db.check_status(app_id) in (False, None):
            raise tornado.web.HTTPError(403)

        pre_body = self._parse_json()
        body = {
            "app_id": app_id,
            "recv_id_list": pre_body["recv_id_list"],
            "badge_cnt_list": pre_body["badge_cnt_list"],
            "show_msg": pre_body["show_msg"],
            "msg": pre_body["msg"]
        }

        self.db.queue.write(jsonmessage.JSONMessage(body=body))
        self.finish()
