# encoding:utf-8
from bmob.api.base import BmobBase


class BmobFile(BmobBase):
    UPLOAD_URL = 'https://api.bmob.cn/2/files'

    def __init__(self, bmob):
        super(BmobFile, self).__init__(bmob)

    def upload(self, filename, file):
        return self.http_post('%s/%s' % (BmobFile.UPLOAD_URL, filename), file)
