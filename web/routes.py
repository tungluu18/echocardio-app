# coding=utf-8
import logging

__author__ = 'Tung.Luu'
_logger = logging.getLogger(__name__)

routing_table = dict({
    'admin': dict({
        'homepage': '/admin/homepage',
        'activate': '/admin/activate/user',
        'delete': '/admin/delete/user',
        'update': '/admin/update/user',
        'session': '/admin/view/user',
        '404': '/admin/404'
    })
})
