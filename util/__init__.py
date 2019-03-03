# coding=utf-8

import logging
import json

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)


def filter_attr(obj, attr):
    return {key: obj[key] for key in (attr & obj.keys())}


def remove_attr(obj, rm_attr):
    return {k: v for k, v in obj.items() if k not in rm_attr}


def valid_req(request, comp_attr=[], ext_attr=[]):
    """ Validate a json request and its attributes
        :param obj request
        :param [str] comp_attr: compulsory attributes
        :param [str] ext_attr: extended attributes
    """
    try:
        req_loaded = json.loads(request.data)
        req_attr = req_loaded.keys()
        if not set(req_attr) >= set(comp_attr):
            raise ValueError('Request must have: ' + ','.join(comp_attr))
        req_filtered = filter_attr(req_loaded, comp_attr + ext_attr)
        return req_filtered
    except Exception as e:
        raise ValueError(
            'Cannot parse request, request format must be application/json!')
