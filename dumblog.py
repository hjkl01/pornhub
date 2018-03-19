#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


class DumbFormatter(logging.Formatter):
    converter = datetime.fromtimestamp

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s,%03d" % (t, record.msecs)
        return s


def dlog(name=__file__, logLevel=None, console='info'):
    name = name.split('/')[-1].split('.')[0]
    logger = logging.getLogger(name)
    levels = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    level = levels.get(logLevel, logging.DEBUG)
    logger.setLevel(level)

    formatter = DumbFormatter(
        '%(asctime)s-%(module)s.%(funcName)s(ln:%(lineno)d) - pid:%(process)d - %(levelname)s :: %(message)s')
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/%s.log' % name, )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if console in levels.keys():
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(levels.get(console, logging.NOTSET))
        console_fmtter = DumbFormatter(
            '%(asctime)s %(module)s-ln:%(lineno)d %(levelname)s :: %(message)s', datefmt='%H:%M:%S,%f')
        stream_handler.setFormatter(console_fmtter)
        logger.addHandler(stream_handler)
    elif not console:
        pass
    else:
        raise Exception('Console Loglevel Error!')

    return logger


if __name__ == '__main__':
    logger = dlog(__file__, logLevel='error', console='info')
    logger.debug('debug')
    logger.info('info')
    logger.error('error')
    logger.critical('critical')
