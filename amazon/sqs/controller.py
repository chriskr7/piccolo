# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 FingerApp Studio, Inc.

from boto import sqs
from boto.sqs.message import Message

from memory.shared.controller import SharedManager


class SQSManager:

    def __init__(self):

        # load config
        config_m = SharedManager.get_config()
        self.config = config_m.config

        self.queue = None

    def get_queue(self):
        if self.queue:
            return self.queue

        sqs_cfg = self.config.queue
        sqs_conn = sqs.connect_to_region(
            aws_access_key_id=sqs_cfg.access_key,
            aws_secret_access_key=sqs_cfg.secret_key,
            region_name=sqs_cfg.region,
            path=sqs_cfg.path)
        self.queue = sqs_conn.get_queue(sqs_cfg.name)
        self.queue.set_message_class(Message)
        return self.queue
