#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 SNMP, Inc.

import sys
from worker.controller import WorkerManager


def main(argv):

    print("Piccolo Worker :)")
    WorkerManager().run()


if __name__ == "__main__":
    main(sys.argv)
