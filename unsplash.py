import json

import requests


class UnsplashSpider:
    def getImage(self):
        client_id = 'de679d87f8bd53dc2ac9b9ab98461179ee998d2092586ddd7e5cdcd78f8cce41'
        searchURL = 'https://api.unsplash.com/photos/random?orientation=landscape&featured=travel'
        header = {'Accept-Version': 'v1', 'Authorization': 'Client-ID %s' % client_id}
        response = requests.get(searchURL, headers=header)
        print('通过UnSplash壁纸源更新...')

        print(response.text)
        data = json.loads(response.text)
        results = data['urls']['full']
        # print(u'正在为您下载图片:%s...' % results)
        return results
