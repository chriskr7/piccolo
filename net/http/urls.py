# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 SNMP, Inc.

from net.http import handlers

handlers = [
    (r"/", handlers.MainHandler),
    (r"/v1/app", handlers.AppHandler),
    (r"/v1/app/user", handlers.UserHandler),
    (r"/v1/app/key", handlers.KeyHandler),
    (r"/v1/app/push", handlers.PushHandler)
]
