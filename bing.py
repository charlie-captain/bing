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
import configparser
import string

filedir_name = ''
file_name = ''
fullfile_name = ''
dir_name = ''
url = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'

is_delete = ''
is_upload = ''
version = ''
update_version = '1.2'
network_state = -1


# check has downloaded
def check():
    global filedir_name
    global file_name
    global fullfile_name
    global dir_name
    dir_name = time.strftime("%Y-%m", time.localtime())
    if not file_exist(dir_name):
        os.mkdir(dir_name)
    file_name = str(time.strftime("%Y-%m-%d", time.localtime())) + '.jpg'
    filedir_name = dir_name + '\\' + file_name
    dir_name = os.path.abspath('.')
    fullfile_name = os.path.join(dir_name, filedir_name)  # 完整路径
    init_config()
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
        if is_upload == '1':
            upload_photos()
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
        if dir == '.git' or dir == '.idea' or dir == 'bmob' or dir == 'dist':
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


# init_config
def init_config():
    global is_delete
    global is_upload
    global version
    conf = configparser.ConfigParser()
    init_file = 'init.ini'
    if not file_exist(init_file):
        conf.add_section('config')
        conf.set('config', 'delete', '0')
        conf.set('config', 'upload', '0')
        conf.set('config', 'version', update_version)
        conf.write(open(init_file, 'w'))
        version = update_version
    else:
        conf.read(init_file)
        is_delete = conf.get('config', 'delete')
        is_upload = conf.get('config', 'upload')
        version = conf.get('config', 'version')


# check update
def update_exe():
    print('检查更新中...')
    json_list = open_url('https://api.github.com/repos/thatnight/bing/contents/dist')
    json_str = json.loads(json_list)
    update_url = ''  # 更新程序下载地址
    for dict in json_str:
        if 'init.ini' == dict['name']:
            print('下载配置文件中...')
            download_file(dict['download_url'], 'init_update.ini', True)
        if 'bing.exe' == dict['name']:
            update_url = dict['download_url']
    print('检查是否更新...')
    conf = configparser.ConfigParser()
    ini_file = 'init_update.ini'
    conf.read(ini_file)
    ini_str = conf.get('config', 'version')
    is_update=False
    if version[0] <= ini_str[0]:
        if version[2] < ini_str[2]:
            print('更新程序中...')
            download_file(update_url, 'bing.exe')
            conf.read('init.ini')
            conf.set('config', 'version', ini_str)
            conf.write(open('init.ini', 'w'))
            is_update=True
    if is_update:
        print('更新完成, 版本号: ' + ini_str)
    else:
        print('程序未更新')
    print('删除更新缓存...')
    os.remove(ini_file)
    print('删除成功')


# download  file
def download_file(url, file_name, text=False):
    file = open_url(url)
    if text:
        with open(file_name, 'w') as f:
            f.write(file.decode())
        return True
    else:
        with open(file_name, 'wb') as f:
            f.write(file)
        return True
    return False

# check the network
def checkNetwork():
    global network_state
    if network_state != 0:
        network_state = os.system('ping www.baidu.com')
    if network_state == 0:
        return True
    return False


if __name__ == '__main__':
    if check():
        print('图片已下载，路径为: ' + fullfile_name)
        refresh_desktop()
    else:
        print('图片不存在.')
        if checkNetwork():
            img_response = open_url(url)
            find_img(img_response)
            update_exe()
        else:
            print('网络连接失败, 请检查连接.')
    if is_delete == '1':
        del_img()
