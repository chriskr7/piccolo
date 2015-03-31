# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 SNMP, Inc.

import pymysql
import time
from datetime import datetime

from logger.controller import LogManager
from memory.shared.controller import SharedManager

from amazon.sqs.controller import SQSManager


class MySQLManager:

    # app status constant
    RUN = "__RUN__"
    STOP = "__STOP__"

    #
    # Query define
    #

    # Register app or user
    _insert_app = "INSERT INTO push_app (app_id, created_time, status) \
                        VALUES (%s, %s, %s)"
    _insert_user = "INSERT INTO push_user \
                               (app_id, uid, device_token, os_type, created_time) \
                         VALUES (%s, %s, %s, %s, %s)"
    _insert_key = "INSERT INTO push_key (app_id, gcm_key, ios_key, ios_cert, created_time) \
                        VALUES (%s, %s, %s, %s, %s)"

    _add_app_user = "UPDATE push_app \
                        SET registered_total_users = registered_total_users + 1 \
                      WHERE app_id = %s"
    _sub_app_user = "UPDATE push_app \
                        SET registered_total_users = registered_total_users - 1 \
                      WHERE app_id = %s"

    # Get app or user info
    _select_app = "SELECT app_id, created_time, timestamp, registered_total_users, \
                          push_cnt, status \
                     FROM push_app \
                    WHERE app_id = %s"
    _select_user = "SELECT uid, device_token, os_type, created_time, timestamp \
                      FROM push_user \
                     WHERE app_id = %s AND uid = %s"
    _select_key = "SELECT gcm_key, ios_key, ios_cert \
                     FROM push_key \
                    WHERE app_id = %s"

    # Modify app's running status or user's device token
    _update_app = "UPDATE push_app \
                      SET status = %s \
                    WHERE app_id = %s"
    _update_user = "UPDATE push_user \
                       SET device_token = %s, \
                           os_type = %s \
                     WHERE app_id = %s AND uid = %s"

    # Delete app or user
    _delete_app_user = "DELETE FROM push_user\
                         WHERE app_id = %s"
    _delete_app = "DELETE FROM push_app \
                         WHERE app_id = %s"
    _delete_user = "DELETE FROM push_user \
                          WHERE app_id = %s AND uid = %s"
    _delete_key = "DELETE FROM push_key \
                         WHERE app_id = %s"

    # Push related
    _select_status = "SELECT status \
                        FROM push_app \
                       WHERE app_id = %s"
    _update_push_cnt = "UPDATE push_app \
                           SET push_cnt = push_cnt + %s \
                         WHERE app_id = %s"

    def __init__(self):

        # load config
        config_m = SharedManager.get_config()
        self.config = config_m.config

        self.conn = None
        self.cursor = None
        self.host = self.config.database.mysql.host
        self.port = self.config.database.mysql.port
        self.user = self.config.database.mysql.user
        self.passwd = self.config.database.mysql.password
        self.db_name = self.config.database.mysql.db_name

        self.queue = SQSManager().get_queue()

        self.dblog = LogManager.get_instance("dblog")

    def connect(self):
        try:
            self.conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                passwd=self.passwd,
                db=self.db_name,
                charset='utf8'
            )
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        except (pymysql.OperationalError, pymysql.InternalError) as e:
            error_code = e.args[0]
            if error_code == 1049:
                self.dblog.error(
                    "Database %s in MySQL not exist!" % self.db_name)
                return False
            else:
                self.dblog.error(
                    "Error occured while connecting to MySQL: %r", e)
                return False

        self.conn.autocommit(True)
        self.dblog.debug("Connecting to MySQL successful")
        return True

    def _ping(self):
        try:
            self.conn.ping()
        except pymysql.OperationalError as e:
            # connection lost
            if e[0] == 2013:
                self.dblog.debug("Reconnecting to MySQL...")
                self.connect()
                self.ping()
                self.dblog.debug("Reconnecting to MySQL successful")
            else:
                self.dblog.error("Error while ping to MySQL: %r", e)
                return False
        return True

    def _datetime_serialize(self, result):
        if type(result) is dict:
            for r in result:
                if isinstance(result[r], (datetime)):
                    result[r] = result[r].strftime('%Y-%m-%d %H:%M:%S')
        elif type(result) is list:
            for row in result:
                for r in row:
                    if isinstance(row[r], (datetime)):
                        row[r] = row[r].strftime('%Y-%m-%d %H:%M:%S')
        return result

    def insert_app(self, app_id):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        self._ping()
        self.cursor.execute(self._insert_app, (app_id, timestamp, self.RUN))
        return {"app_id": app_id, "created_time": timestamp} \
            if self.conn.affected_rows() == 1 else None

    def insert_user(self, app_id, uid, dev_token, os_type):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        self._ping()
        self.cursor.execute(self._insert_user, (app_id, uid, dev_token, os_type, timestamp))
        if self.conn.affected_rows() != 1:
            return None
        self.cursor.execute(self._add_app_user, app_id)
        return {"uid": uid, "created_time": timestamp} \
            if self.conn.affected_rows() == 1 else None

    def insert_key(self, app_id, gcm_key, ios_key, ios_cert):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        self._ping()
        self.cursor.execute(self._insert_key, (app_id, gcm_key, ios_key, ios_cert, timestamp))
        return {"app_id": app_id, "created_time": timestamp} \
            if self.conn.affected_rows() == 1 else None

    def select_app(self, app_id):
        self._ping()
        self.cursor.execute(self._select_app, app_id)
        row = self.cursor.fetchone()
        return self._datetime_serialize(row) if row else None

    def select_user(self, app_id, uid):
        self._ping()
        self.cursor.execute(self._select_user, (app_id, uid))
        row = self.cursor.fetchone()
        return self._datetime_serialize(row) if row else None

    def select_key(self, app_id):
        self._ping()
        self.cursor.execute(self._select_key, app_id)
        row = self.cursor.fetchone()
        return {"gcm_key": row["gcm_key"], "ios_key": row["ios_key"], "ios_cert": row["ios_cert"]} \
            if row else None

    def update_app(self, app_id, status):
        self._ping()
        self.cursor.execute(self._update_app, (status, app_id))
        if self.cursor.rowcount != 1:
            return None
        rslt = self.select_app(app_id)
        return {"app_id": rslt["app_id"], "timestamp": rslt["timestamp"],
                "status": rslt["status"]}

    def update_user(self, app_id, uid, dev_token, os_type):

        self.cursor.execute(self._update_user, (dev_token, os_type, app_id, uid))
        if self.cursor.rowcount != 1:
            return None
        rslt = self.select_user(app_id, uid)
        return {"uid": rslt["uid"], "dev_token": rslt["device_token"],
                "os_type": rslt["os_type"], "timestamp": rslt["timestamp"]}

    def check_status(self, app_id):
        self._ping()
        self.cursor.execute(self._select_status, app_id)
        row = self.cursor.fetchone()
        return row["status"] == self.RUN if row else None

    def add_push_cnt(self, app_id, cnt):
        self._ping()
        self.cursor.execute(self._update_push_cnt, (cnt, app_id))
        if self.cursor.rowcount != 1:
            self.dblog.debug("rowcount: %d" % self.cursor.rowcount)
            return False
        return True

    def delete_app(self, app_id):
        self._ping()
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute(self._delete_app_user, app_id)
        self.cursor.execute(self._delete_app, app_id)
        return {"app_id": app_id, "timestamp": timestamp} \
            if self.conn.affected_rows() == 1 else None

    def delete_user(self, app_id, uid):
        self._ping()
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute(self._delete_user, (app_id, uid))
        if self.conn.affected_rows() != 1:
            return None
        self.cursor.execute(self._sub_app_user, app_id)
        return {"uid": uid, "timestamp": timestamp} \
            if self.conn.affected_rows() == 1 else None

    def delete_key(self, app_id):
        self._ping()
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute(self._delete_key, app_id)
        return {"app_id": app_id, "timestamp": timestamp} \
            if self.conn.affected_rows() == 1 else None

    def disconnect(self):
        if self.conn:
            self.dblog.debug("Closing connection to MySQL")
            self.conn.close()

    def __del__(self):
        self.disconnect()
