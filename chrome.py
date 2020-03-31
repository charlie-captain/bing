import json
import random

url_360 = 'http://wallpaper.apc.360.cn/index.php?c=WallPaper&a=getAppsByOrder&order=create_time&start=0&count={0}&from=360chrome'

count = 50


def open_chrome_url():
    print('通过360壁纸源更新...')
    api_url = url_360.format(str(count))
    from bing import open_url
    api_response = open_url(api_url)
    return deal_response(api_response)


def deal_response(json_str):
    index = random.randint(0, count)
    json_data = json.loads(json_str)
    data_list = json_data['data']
    img_data = data_list[index]
    while not img_data:
        print('数据源失效')
        index = random.randint(0, count)
        img_data = json_data[index]
    download_url = img_data['url']
    return download_url
