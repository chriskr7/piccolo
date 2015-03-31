#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 FingerApp Studio, Inc.

import sys

from tornado import options

from net.http.controller import PushHttpServer
from logger.controller import LogManager


def print_usage(fname):
    print("Usage: %s [config] [task_id=optional]" % fname)
    sys.exit()


def main(argv):

    print("SNMP API Server")

    if len(argv) < 2:
        print_usage(argv[0])

    options.parse_command_line()
    task_id = 0
    config_file = argv[1]

    if len(argv) > 2:
        task_id = int(argv[2])

    # http server instance
    push_http_server = PushHttpServer(
        config_file=config_file,
        task_id=task_id
    )

    # enable log
    push_http_server.enable_log()

    general = LogManager.get_instance("general")
    general.debug("Piccolo API Server is started in %s mode..."
                  % push_http_server.stage)
    general.debug("Task ID : %d" % push_http_server.task_id)
    general.debug("HTTP listen port : %d" % push_http_server.listen_port)

    # run
    push_http_server.run()

    return True


if __name__ == "__main__":
    main(sys.argv)
