# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 SNMP, Inc.

from tornado import httpserver
from tornado import ioloop
from tornado import web

from config.controller import ConfigManager
from logger.controller import LogManager
from memory.shared.controller import SharedManager
from database.mysql.controller import MySQLManager


class Application(web.Application):
    pass


class PushHttpServer(Application):

    def __init__(self, config_file, task_id=0):
        self.config_m = ConfigManager(config_file=config_file, task_id=task_id)
        SharedManager.load(self.config_m)

        self.config = self.config_m.config
        self._task_id = task_id
        self._listen_port = self.config.server.base_port + task_id
        self._stage = self.config.application.stage
        self._version = self.config.application.version
        self.application = None

    def __del__(self):
        SharedManager.destroy()

    def _build_url_handlers(self):
        from net.http import urls as push_urls
        handlers = push_urls.handlers
        return handlers

    def _init_http_server(self):
        if self.config is None:
            return False

        self.application = Application(
            handlers=None,
            debug=self.config.debug,
            config=self.config
        )

        self.application.db = MySQLManager()
        self.application.db.connect()

        for host_name in self.config.server.hosts:
            self.application.add_handlers(
                host_name.host,
                self._build_url_handlers()
            )

        self.ssl_options = None
        if self.config.server.ssl.cert_filename\
                and self.config.server.ssl.key_filename:
            self.ssl_options = {
                "certfile": self.config.server.ssl.cert_filename,
                "keyfile": self.config.server.ssl.key_filename
            }
        return True

    def enable_log(self):
        LogManager.enable_http_log()

    @property
    def task_id(self):
        return self._task_id

    @task_id.setter
    def task_id(self, value):
        raise AttributeError("task_id is not settable!")

    @property
    def stage(self):
        return self._stage

    @stage.setter
    def stage(self, value):
        raise AttributeError("stage is not settable!")

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        raise AttributeError("version is not settable!")

    @property
    def listen_port(self):
        return self._listen_port

    @listen_port.setter
    def listen_port(self, value):
        raise AttributeError("listen_port is not settable!")

    def run(self):
        if self._init_http_server() is True:
            http_server = httpserver.HTTPServer(
                self.application,
                ssl_options=self.ssl_options
            )
            http_server.listen(self._listen_port)
            ioloop.IOLoop.instance().start()
        self.application.db.disconnect()
