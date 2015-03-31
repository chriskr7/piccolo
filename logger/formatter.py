# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 FingerApp Studio, Inc.

import sys
import time

import logging

from tornado.escape import _unicode
from tornado.util import unicode_type, basestring_type

try:
    import curses
except ImportError:
    curses = None


class LogFormatter(logging.Formatter):

    def __init__(self, task_id=0, color=True, *args, **kwargs):
        super(LogFormatter, self).__init__(*args, **kwargs)

        self._task_id = task_id
        self._color = color and self._stderr_supports_color()
        if self._color:
            fg_color = (curses.tigetstr("setaf") or
                        curses.tigetstr("setf") or "")
            if (3, 0) < sys.version_info < (3, 2, 3):
                fg_color = unicode_type(fg_color, "ascii")
            self._colors = {
                # Blue
                logging.DEBUG: unicode_type(curses.tparm(fg_color, 4),
                                            "ascii"),
                # Green
                logging.INFO: unicode_type(curses.tparm(fg_color, 2),
                                           "ascii"),
                # Yellow
                logging.WARNING: unicode_type(curses.tparm(fg_color, 3),
                                              "ascii"),
                # Red
                logging.ERROR: unicode_type(curses.tparm(fg_color, 1),
                                            "ascii"),
            }
            self._normal = unicode_type(curses.tigetstr("sgr0"), "ascii")

    def _stderr_supports_color():
        color = False
        if curses and sys.stderr.isatty():
            try:
                curses.setupterm()
                if curses.tigetnum("colors") > 0:
                    color = True
            except Exception:
                pass
        return color

    def format(self, record):
        try:
            record.message = record.getMessage()
        except Exception as e:
            record.message = "Bad message (%r): %r" % (e, record.__dict__)
        assert isinstance(record.message, basestring_type)

        record.task_id = self._task_id
        record.asctime = time.strftime(
            "%y%m%d %H:%M:%S", self.converter(record.created))
        prefix = "[%(task_id)d %(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]" % \
            record.__dict__
        if self._color:
            prefix = (self._colors.get(record.levelno, self._normal) +
                      prefix + self._normal)

        def safe_unicode(s):
            try:
                return _unicode(s)
            except UnicodeDecodeError:
                return repr(s)

        formatted = prefix + " " + safe_unicode(record.message)
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            lines = [formatted.rstrip()]
            lines.extend(
                safe_unicode(ln) for ln in record.exc_text.split('\n'))
            formatted = '\n'.join(lines)
        return formatted.replace("\n", "\n    ")
