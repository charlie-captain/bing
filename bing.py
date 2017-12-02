# 下载每日必应壁纸
import urllib.request
import json
import time
import win32gui
import win32con
import os
import shutil
import winwalls

# connect to the url
def open_url(url):
    request = urllib.request.Request(url)
    request.add_header('User-Agent',
                       'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3357.400 QQBrowser/9.6.11858.400')
    response = urllib.request.urlopen(request)
    return response.read()


# download image
def find_img(response_html):
    print('正在下载图片...')
    jsons = json.loads(response_html)
    img_dict = jsons['images']
    img = img_dict[0]
    if img['url']:
        save_img(img['url'])


# save picture
def save_img(img_url):
    url_pic = 'http://cn.bing.com' + img_url
    dir_name = time.strftime("%Y-%m", time.localtime())
    if not file_exist(dir_name):
        os.mkdir(dir_name)
    file_name = dir_name + '/' + str(time.strftime("%Y-%m-%d", time.localtime())) + '.jpg'
    img = open_url(url_pic)
    if img and not file_exist(file_name):
        with open(file_name, 'wb') as f:
            f.write(img)
        print('图片下载成功, 正在设置为壁纸...')
        update_img(file_name)
        print('壁纸设置成功.')
    else:
        print('图片已存在.')


# find the file
def file_exist(file_name):
    temp = os.path.exists(file_name)
    return temp


# change the destop
def update_img(file_name):
    dir_name = os.path.abspath('.')
    print(dir_name)
    img_path = os.path.join(dir_name, file_name)
    print(img_path)
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, img_path, 1 + 2)


# delete picture per month
def del_img():
    now_date = time.strftime("%Y-%m")
    dirs = [x for x in os.listdir('.') if os.path.isdir(x)]
    print(dirs)
    for dir in dirs:
        if dir == '.git' or dir == '.idea':
            continue
        if dir != now_date:
            shutil.rmtree(dir)


url = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
img_response = open_url(url)
find_img(img_response)
del_img()
