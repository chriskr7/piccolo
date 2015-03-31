# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 FingerApp Studio, Inc.

import json
import yaml

from config import models


class ConfigManager:

    def __init__(self, config_file, task_id=0):
        with open(config_file) as fp:
            opt = yaml.load(fp)
        self._config = models.AppConfig.from_json(json.dumps(opt))
        self._task_id = task_id

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        raise AttributeError("config is not settable!")

    @property
    def task_id(self):
        return self._task_id

    @task_id.setter
    def task_id(self, value):
        raise AttributeError("task_id is not settable!")
