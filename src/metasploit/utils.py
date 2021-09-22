#!/usr/bin/env python

from optparse import OptionParser

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2021, PyMetasploit Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '2.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

__all__ = [
    'parseargs'
]


def parseargs():
    p = OptionParser()
    p.add_option("-P", dest="password", help="Specify the password to access msfrpcd", metavar="opt")
    p.add_option("-S", dest="ssl", help="Disable SSL on the RPC socket", action="store_false", default=True)
    p.add_option("-U", dest="username", help="Specify the username to access msfrpcd", metavar="opt", default="msf")
    p.add_option("-a", dest="server", help="Connect to this IP address", metavar="host", default="127.0.0.1")
    p.add_option("-p", dest="port", help="Connect to the specified port instead of 55553", metavar="opt", default=55553)
    o, a = p.parse_args()
    if o.password is None:
        print('[-] Error: a password must be specified (-P)\n')
        p.print_help()
        exit(-1)
    return o


def convert_bytes_to_string(bytes_dict: dict) -> dict:
    """
    :param bytes_dict: dictionary, where inner objects are strings, bytes, or collections of those types
    :return: original dictionary with any bytes values converted to strings
    """
    str_data = {}
    if isinstance(bytes_dict, dict):
        for key, val in bytes_dict.items():
            if isinstance(key, bytes):
                key_temp = key.decode()
            else:
                key_temp = key
            if isinstance(val, list) or isinstance(val, tuple):
                val_temp = convert_val(val)
            elif isinstance(val, dict):
                val_temp = convert_bytes_to_string(val)
            elif isinstance(val, bytes):
                val_temp = val.decode()
            else:
                val_temp = val
            str_data[key_temp] = val_temp
    return str_data


def convert_val(bytes_obj: iter):
    """
    :param bytes_obj: some object containing either string or byte values, can be collection or just bytes
    :return: object containing original strings and converted bytes to strings
    """
    for index, item in enumerate(bytes_obj):
        if isinstance(item, bytes):
            bytes_obj[index] = item.decode('utf-8')
        elif isinstance(item, dict):
            item = convert_bytes_to_string(item)
            bytes_obj[index] = item
        elif isinstance(item, tuple) or isinstance(item, list):
            bytes_obj[index] = convert_val(item)
    return bytes_obj
