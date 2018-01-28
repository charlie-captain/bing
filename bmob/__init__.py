# encoding:utf-8
from bmob.api.file import BmobFile


class Bmob(object):
    def __init__(self, app_id=None, rest_api_key=None, secret_key=None, force_config=False):
        super(Bmob, self).__init__()
        self.app_id = app_id
        self.rest_api_key = rest_api_key
        self.secret_key = secret_key

        self._file = None

    @property
    def file(self):
        if not self._file:
            self._file = BmobFile(self)
        return self._file
