#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 FingerApp Studio, Inc.

import sys
import time

from amazon.sqs.controller import SQSManager


def main(argv):
    queue = SQSManager().get_queue()

    cnt_flag = 0

    while True:
        if cnt_flag == 100:
            break
        msgs = queue.get_messages(10)
        for msg in msgs:
            queue.delete_message(msg)
        time.sleep(2)
        cnt_flag += 1

    print("Clearing Queue Completed!")

if __name__ == "__main__":
    main(sys.argv)
