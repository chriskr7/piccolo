# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 SNMP, Inc.

import pickle
import sysv_ipc

from config.signature import SigGenerator


class SharedManager:
    MEMORY_KEY = 7272

    APP_GET = 'GET+/1/app'
    APP_POST = 'POST+/1/app'
    APP_PUT = 'PUT+/1/app'
    APP_DELETE = 'DELETE+/1/app'

    USER_GET = 'GET+/1/app/user'
    USER_POST = 'POST+/1/app/user'
    USER_PUT = 'PUT+/1/app/user'
    USER_DELETE = 'DELETE+/1/app/user'

    KEY_POST = 'POST+1/app/key'
    KEY_DELETE = 'DELETE+1/app/key'

    PUSH = 'PUSH+/1/app/push'
    memory = None

    @staticmethod
    def load(config_class):

        config = config_class.config
        secret_key = config.apikey.secret

        config.apikey.app.get = SigGenerator.generate(secret_key, SharedManager.APP_GET)
        config.apikey.app.post = SigGenerator.generate(secret_key, SharedManager.APP_POST)
        config.apikey.app.put = SigGenerator.generate(secret_key, SharedManager.APP_PUT)
        config.apikey.app.delete = SigGenerator.generate(secret_key, SharedManager.APP_DELETE)

        config.apikey.user.get = SigGenerator.generate(secret_key, SharedManager.USER_GET)
        config.apikey.user.post = SigGenerator.generate(secret_key, SharedManager.USER_POST)
        config.apikey.user.put = SigGenerator.generate(secret_key, SharedManager.USER_PUT)
        config.apikey.user.delete = SigGenerator.generate(secret_key, SharedManager.USER_DELETE)

        config.apikey.key.post = SigGenerator.generate(secret_key, SharedManager.KEY_POST)
        config.apikey.key.delete = SigGenerator.generate(secret_key, SharedManager.KEY_DELETE)

        config.apikey.push = SigGenerator.generate(secret_key, SharedManager.PUSH)

        pickled_config = pickle.dumps(config_class)

        SharedManager.memory = sysv_ipc.SharedMemory(
            SharedManager.MEMORY_KEY, sysv_ipc.IPC_CREAT, size=sysv_ipc.PAGE_SIZE)
        SharedManager.memory.write(pickled_config, offset=0)

    @staticmethod
    def get_config():
        if SharedManager.memory is None:
            SharedManager.memory = sysv_ipc.SharedMemory(SharedManager.MEMORY_KEY)
        raw_object = SharedManager.memory.read()
        return pickle.loads(raw_object)

    @staticmethod
    def destroy():
        sysv_ipc.remove_shared_memory(SharedManager.MEMORY_KEY)
