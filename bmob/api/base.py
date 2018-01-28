# encoding:utf-8
import json
import mimetypes
from urllib import request

mimetypes.init(["mimetypes.txt"])


class BmobBase(object):
    def __init__(self, bmob):
        self.bmob = bmob

    def http_post(self, url, body, parse=True):
        mtype = mimetypes.guess_type(url)
        headers = {
            'X-Bmob-Application-Id': self.bmob.app_id,
            'X-Bmob-REST-API-Key': self.bmob.rest_api_key,
            'Content-Type': mtype[0]
        }
        req = request.Request(url, data=body, headers=headers)
        self.http_add_headers(req)
        res = request.urlopen(req)
        body = res.read().decode("utf-8")
        if parse:
            return json.loads(body, object_hook=_obj_hook)
        return res

    def http_add_headers(self, req):
        """Sub class rewiter this function If it's necessary to add headers"""
        pass


class JsonObject(dict):
    """
    general json object that can bind any fields but also act as a dict.
    """

    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value


def _obj_hook(pairs):
    """
    convert json object to python object.
    """
    o = JsonObject()
    for k, v in pairs.items():
        o[str(k)] = v
    return o
