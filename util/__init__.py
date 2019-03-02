# coding=utf-8

import logging

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)


def filter_attr(obj, attr):
    return {key: obj[key] for key in attr}


def remove_attr(obj, rm_attr):
    return {k: v for k, v in obj.items() if k not in rm_attr}
