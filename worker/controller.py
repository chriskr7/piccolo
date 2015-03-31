# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 SNMP, Inc.

import json
import time

from amazon.sqs.controller import SQSManager
from database.mysql.controller import MySQLManager
from logger.controller import LogManager

from gcm import GCM
from apns import APNs, Payload


class WorkerManager:

    _APN_ = {}
    _GCM_ = {}

    delay_time = 1

    def __init__(self):
        self.queue = SQSManager().get_queue()
        self.database = MySQLManager()
        self.database.connect()
        self.logger = LogManager.get_instance("application")

    def _process(self):
        msgs = self.queue.get_messages(10)

        if len(msgs) > 0:
            for msg in msgs:
                try:
                    msg_body = msg.get_body()

                    data = json.loads(msg_body)
                    app_id = data["app_id"]
                    recv_id_list = data["recv_id_list"]
                    badge_cnt_list = data["badge_cnt_list"]
                    push_msg = data["msg"]
                    show_msg = data["show_msg"]

                    # load application's gcm & apn keys
                    self._load_push_keys(app_id)

                    android_recv_list = []

                    for recv_id, badge_cnt in zip(recv_id_list, badge_cnt_list):
                        query = self.database.select_user(app_id, recv_id)
                        if query is None:
                            self.logger.warning("Warning: %s is not in %s app!" % (recv_id, app_id))
                            continue
                        if query["os_type"] == "A":
                            # push multicast to gcm limited to at most 1000
                            if len(android_recv_list) < 990:
                                android_recv_list.append(query["device_token"])
                            else:
                                android_recv_list.append(query["device_token"])
                                self._andorid_push(app_id, android_recv_list, push_msg)
                                android_recv_list = []
                        elif query["os_type"] == "I":
                            self._push_ios(
                                app_id, query["device_token"], push_msg, show_msg, badge_cnt)

                    if len(android_recv_list) > 0:
                        self._push_android(app_id, android_recv_list, push_msg)
                    self.queue.delete_message(msg)
                except Exception as e:
                    self.logger.error("Error: %s", str(e))
                    pass
            self.delay_time = 1
        else:
            time.sleep(self.delay_time)
            self.delay_time = (self.delay_time + 1) if self.delay_time < 20 else self.delay_time

    def _load_push_keys(self, app_id):
        if app_id in self._APN_ and app_id in self._GCM_:
            return
        keyset = self.database.select_key(app_id)
        self._APN_[app_id] = APNs(
            use_sandbox=True, cert_file=keyset["ios_cert"], key_file=keyset["ios_key"])
        self._GCM_[app_id] = GCM(keyset["gcm_key"])

    def _push_android(self, app_id, recv_list, push_msg):
        try:
            self._GCM_[app_id].json_request(registration_ids=recv_list, data=push_msg)
            if self.database.add_push_cnt(app_id, len(recv_list)) is False:
                self.logger.warning("Warning: push count did not added[app_id: %s]" % app_id)
        except Exception as e:
            self.logger.error("Error: %s", str(e))

    def _push_ios(self, app_id, recv_token, push_msg, show_msg, badge_cnt):
        try:
            payload = Payload(alert=show_msg, sound="defalt", custom=push_msg, badge=badge_cnt)
            self._APN_[app_id].gateway_server.send_notification(recv_token, payload)
            self.database.add_push_cnt(app_id, 1)
        except Exception as e:
            self.logger.error("Error: %s", str(e))

    def run(self):
        while True:
            self._process()
        self.database.disconnect()
