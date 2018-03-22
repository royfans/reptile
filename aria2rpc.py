# coding: utf-8

import time
import requests
from requests.exceptions import HTTPError

import logging
app_log = logging.getLogger('Beibei')
app_log.setLevel(logging.INFO)

ARIA2_RPC_URL = 'http://localhost:6800/jsonrpc'

def jsonrpc(method, params):
    app_log.debug('aria2 rpc method: %s', method)
    req_id = str(time.time())
    req_data = {'jsonrpc': '2.0', 'id': req_id,
                'method': 'aria2.' + method,
                'params': params}
    try:
        res = requests.post(ARIA2_RPC_URL, json=req_data, proxies={'http': None})
        res.raise_for_status()
        data = res.json()
        return data['result']
    except HTTPError as e:
        app_log.error(e)
        raise e
    except Exception as e:
        app_log.error(e)
        raise e

def rpc_addUri(uri, options):
    # options => {'out': filename}
    if isinstance(uri, (list, tuple)):
        uris = uri
    else:
        uris = [uri]
    return jsonrpc('addUri', [uris, options])

def rpc_remove(gid):
    return jsonrpc('remove', [gid])

def rpc_removeDownloadResult(gid):
    return jsonrpc('removeDownloadResult', [gid])

def rpc_getFiles(gid):
    return jsonrpc('getFiles', [gid])

def rpc_getOption(gid):
    return jsonrpc('getOption', [gid])

def rpc_tellStatus(gid):
    return jsonrpc('tellStatus', [gid, ['gid',
        'status', 'files', 'completedLength', 'errorCode']])

def rpc_tellStopped(num=1000):
    return jsonrpc('tellStopped', [0, num])

def rpc_getGlobalOption():
    return jsonrpc('getGlobalOption', [])

def rpc_getGlobalStat():
    return jsonrpc('getGlobalStat', [''])

def add_aria2_task(url, filename):
    try:
        result = rpc_addUri(url, ''.join(['url_', filename, '.apk']))
        return result
    except Exception as e:
        print(e)
        return None

def get_file_status(gid):
    try:
        result = rpc_tellStatus(gid)
        return result
    except Exception as e:
        print(e)
        return None

def remove_dl_result(gid):
    try:
        result = jsonrpc('removeDownloadResult', [gid])
        return result
    except Exception as e:
        print(e)
        return None

def get_global_stat():
    try:
        result = jsonrpc('getGlobalStat', [])
        return result
    except Exception as e:
        print(e)
        return None