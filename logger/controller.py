# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 FingerApp Studio, Inc.

import errno
import logging
import logging.handlers
import os

from memory.shared.controller import SharedManager
from logger.formatter import LogFormatter


class LogManager:
    access = None
    application = None
    general = None
    dblog = None

    options = dict(
        log_file_max_size=1024 * 1024,
        log_file_num_backups=100,
        log_to_stderr=False
    )

    @staticmethod
    def _enable_pretty_logging(logger=None, options=None, task_id=0):
        if options is None:
            return
        if options["logging"] == "none":
            return

        if logger is None:
            logger = logging.getLogger()

        logger.setLevel(
            getattr(logging, options["logging"].upper()))

        if options["log_file_prefix"]:
            channel = logging.handlers.RotatingFileHandler(
                filename=options["log_file_prefix"],
                maxBytes=options["log_file_max_size"],
                backupCount=options["log_file_num_backups"])
            channel.setFormatter(
                LogFormatter(task_id=task_id, color=False))
            logger.addHandler(channel)

        # Not used with our LogManager, just keep for possible laster use
        if (LogManager.options["log_to_stderr"] or
                (LogManager.options["log_to_stderr"] is None and
                    not logger.handlers)):
            channel = logging.StreamHandler()
            channel.setFormatter(
                LogFormatter(task_id=task_id, color=True))
            logger.addHandler(channel)

    @staticmethod
    def _build_canonical_file_path(base_path, filename):
        try:
            if not os.path.isdir(base_path):
                os.makedirs(base_path, 0o755)
        except OSError as e:
            if e.errno == errno.EEXIST and os.path.isdir(base_path):
                pass
            else:
                raise

        canonical_file_path = base_path
        if not canonical_file_path.endswith("/"):
            canonical_file_path += "/"
        canonical_file_path += filename

        return canonical_file_path

    @staticmethod
    def enable_access_log():
        # load config
        config_m = SharedManager.get_config()
        config = config_m.config
        task_id = config_m.task_id

        LogManager.access = logging.getLogger("tornado.access")
        canonical_file_path = LogManager._build_canonical_file_path(
            base_path=config.logging.access.path,
            filename=config.logging.access.filename
        )
        LogManager.options["logging"] = config.logging.access.level
        LogManager.options["log_file_prefix"] = canonical_file_path
        LogManager._enable_pretty_logging(
            logger=LogManager.access,
            options=LogManager.options,
            task_id=task_id
        )

    @staticmethod
    def enable_application_log():
        # load config
        config_m = SharedManager.get_config()
        config = config_m.config
        task_id = config_m.task_id

        LogManager.application = logging.getLogger("tornado.application")
        canonical_file_path = LogManager._build_canonical_file_path(
            base_path=config.logging.application.path,
            filename=config.logging.application.filename
        )
        LogManager.options["logging"] = config.logging.application.level
        LogManager.options["log_file_prefix"] = canonical_file_path
        LogManager._enable_pretty_logging(
            logger=LogManager.application,
            options=LogManager.options,
            task_id=task_id
        )

    @staticmethod
    def enable_general_log():
        # load config
        config_m = SharedManager.get_config()
        config = config_m.config
        task_id = config_m.task_id

        LogManager.general = logging.getLogger("tornado.general")
        canonical_file_path = LogManager._build_canonical_file_path(
            base_path=config.logging.general.path,
            filename=config.logging.general.filename
        )
        LogManager.options["logging"] = config.logging.general.level
        LogManager.options["log_file_prefix"] = canonical_file_path
        LogManager._enable_pretty_logging(
            logger=LogManager.general,
            options=LogManager.options,
            task_id=task_id
        )

    @staticmethod
    def enable_http_log():
        # access log
        LogManager.enable_access_log()

        # application log
        LogManager.enable_application_log()

        # general log
        LogManager.enable_general_log()

    @staticmethod
    def enable_db_log():
        # load config
        config_m = SharedManager.get_config()
        config = config_m.config
        task_id = config_m.task_id

        LogManager.dblog = logging.getLogger("pushgram.mysql")
        canonical_file_path = LogManager._build_canonical_file_path(
            base_path=config.logging.mysql.path,
            filename=config.logging.mysql.filename
        )
        LogManager.options["logging"] = config.logging.mysql.level
        LogManager.options["log_file_prefix"] = canonical_file_path
        LogManager._enable_pretty_logging(
            logger=LogManager.dblog,
            options=LogManager.options,
            task_id=task_id
        )

    @staticmethod
    def _get_access():
        if not LogManager.access:
            LogManager.enable_access_log()
        return LogManager.access

    @staticmethod
    def _get_application():
        if not LogManager.application:
            LogManager.enable_application_log()
        return LogManager.application

    @staticmethod
    def _get_general():
        if not LogManager.general:
            LogManager.enable_general_log()
        return LogManager.general

    @staticmethod
    def _get_dblog():
        if not LogManager.dblog:
            LogManager.enable_db_log()
        return LogManager.dblog

    @staticmethod
    def get_instance(logger_name):
        if logger_name is None:
            return None

        logger_map = {
            "access": LogManager._get_access,
            "application": LogManager._get_application,
            "general": LogManager._get_general,
            "dblog": LogManager._get_dblog
        }
        if logger_name in logger_map:
            return logger_map[logger_name]()
        else:
            return logging.getLogger()
