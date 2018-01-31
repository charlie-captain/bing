# 下载每日必应壁纸
import urllib.request
import json
import time
import win32con
import win32gui
import os
import shutil
import winwalls
from bmob import Bmob

filedir_name = ''
file_name = ''
fullfile_name = ''
url = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'


# check has downloaded
def check():
    global filedir_name
    global file_name
    global fullfile_name
    dir_name = time.strftime("%Y-%m", time.localtime())
    if not file_exist(dir_name):
        os.mkdir(dir_name)
    file_name = str(time.strftime("%Y-%m-%d", time.localtime())) + '.jpg'
    filedir_name = dir_name + '\\' + file_name
    dir_name = os.path.abspath('.')
    fullfile_name = os.path.join(dir_name, filedir_name)  # 完整路径
    if file_exist(filedir_name):
        return True
    return False


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
    img = open_url(url_pic)
    if img and not file_exist(filedir_name):
        with open(filedir_name, 'wb') as f:
            f.write(img)
        print('图片下载成功.')
        #upload_photos()
    else:
        print('图片已存在.')
    print('文件完整路径为:' + fullfile_name)
    refresh_desktop()  # 存不存在都要更换壁纸


# find the file
def file_exist(file_name):
    temp = os.path.exists(file_name)
    return temp


# change the desktop
def refresh_desktop():
    print('正在设置为壁纸...')
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, fullfile_name, 1 + 2)
    print('壁纸设置成功.')


# delete picture per month
def del_img():
    print('删除非本月壁纸，清理缓存...')
    now_date = time.strftime("%Y-%m")
    dirs = [x for x in os.listdir('.') if os.path.isdir(x)]
    # print(dirs)
    for dir in dirs:
        if dir == '.git' or dir == '.idea' or dir == 'bmob':
            continue
        if dir != now_date:
            shutil.rmtree(dir)
            print('删除文件夹：' + dir)


# upload photos to bmob
def upload_photos():
    print('正在上传壁纸到bmob...')
    bmob = Bmob(app_id='aceac6d6b11815af5a497b2f917d5cd0',
                rest_api_key='459df02fdb3dfe94b0f87c7f96e69ff0',
                secret_key='774eb693e6efefdf')
    file = open(fullfile_name, 'rb')
    try:
        res = bmob.file.upload(file_name, file.read())
        # str = str(res)
        # print('返回数据: ' + str)
    finally:
        file.close()


if __name__ == '__main__':
    if check():
        print('图片已下载，路径为: ' + fullfile_name)
        refresh_desktop()
    else:
        print('图片不存在.')
        img_response = open_url(url)
        find_img(img_response)
    del_img()
