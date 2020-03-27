# 下载每日必应壁纸
import configparser
import json
import os
import shutil
import subprocess
import time
import traceback
import urllib.request
from contextlib import closing

import requests
import win32api
import win32con
import win32gui

import chrome
from bmob import Bmob

filedir_name = ''
file_name = ''
fullfile_name = ''
dir_name = ''
url = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&nc=1585280936631&pid=hp&mkt=zh-CN&video=1&uhd=1&uhdwidth=3360&uhdheight=1890'

source = '0'
is_delete = '1'
is_upload = '1'
is_auto_run = '1'
version = '0'
update_version = '1.5'
# 强制刷新
force_update = '1'
# update version
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
    print('图片不存在.')
    return False


# connect to the url
def open_url(url):
    request = urllib.request.Request(url)
    request.add_header('User-Agent',
                       'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3357.400 QQBrowser/9.6.11858.400')
    response = urllib.request.urlopen(request)
    return response.read()


# download image
def deal_bing(response_html):
    print('正在下载图片...')
    jsons = json.loads(response_html)
    img_dict = jsons['images']
    img = img_dict[0]
    return 'http://cn.bing.com' + img['url']


# save picture
def download_img(img_url):
    print('图片下载地址 ' + img_url)
    img = open_url(img_url)
    if file_exist(filedir_name):
        os.remove(filedir_name)

    if img:
        with open(filedir_name, 'wb') as f:
            f.write(img)
        print('图片下载成功.')
        if is_upload == 1:
            upload_photos()
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
    global is_auto_run
    global source
    global force_update
    conf = configparser.ConfigParser()
    init_file = 'init.ini'
    if not file_exist(init_file):
        conf.add_section('config')
        conf.set('config', 'delete', '0')
        conf.set('config', 'upload', '1')
        conf.set('config', 'auto_run', '1')
        conf.set('config', 'version', str(update_version))
        conf.set('config', 'source', '1')
        conf.set('config', 'force_update', '1')
        conf.write(open(init_file, 'w'))
        version = update_version
    else:
        conf.read(init_file)
        is_delete = conf.get('config', 'delete', fallback=is_delete)
        is_upload = conf.get('config', 'upload', fallback=is_upload)
        is_auto_run = conf.get('config', 'auto_run', fallback=is_auto_run)
        source = conf.get('config', 'source', fallback=source)
        version = conf.get('config', 'version', fallback=update_version)
        force_update = conf.get('config', 'force_update', fallback=force_update)


# check update
def update_exe():
    print('检查更新中...')
    json_list = open_url('https://raw.githubusercontent.com/charlie-captain/bing/master/release')
    print(json_list)
    json_str = json.loads(json_list)
    update_url = json_str['url']  # 更新程序下载地址
    new_version = json_str['version']
    print('检查是否更新...')
    is_update = False
    print('最新版本: ' + str(new_version))
    print('当前版本: ' + str(version))
    if new_version > float(version):
        download_progress(update_url, 'bing.exe')
        is_update = True
    if is_update:
        print('更新完成, 版本号: ' + str(new_version))
    else:
        print('程序未更新')


def download_progress(url, file_name):
    count = 0
    with closing(requests.get(url, stream=True)) as r:
        per_size = 1024
        file_size = int(r.headers['content-length'])
        # progress = ProgressBar(file_name, total=file_size,
        #                        unit='KB', chunk_size=per_size
        #                        , run_status='正在下载', fin_status='下载完成')
        with open(file_name, 'wb') as f:
            for data in r.iter_content(chunk_size=per_size):
                f.write(data)
                count = count + per_size
                next = str(round(count / file_size * 100, 2)) + ' %'
                print(next)
                # progressbar.ProgressBar(len(data))
                # time.sleep(0.01)
                # progress.refresh(count=len(data))


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
    print("检查网络状态")
    if network_state != 0:
        network_state = subprocess.call('ping www.baidu.com', shell=True)
    if network_state == 0:
        print("网络状态正常")
        return True
    return False


def autoRun():
    name = 'bing'  # 要添加的项值名称
    path = os.getcwd() + '\\' + 'bing.exe'  # 要添加的exe路径
    # 注册表项名
    KeyName = 'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
    print('自启动程序路径: ' + path)
    if not file_exist(path):
        print('程序不存在, 无法添加自启动')
        return
    # 异常处理
    try:
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
        win32api.RegSetValueEx(key, name, 0, win32con.REG_SZ, path)
        win32api.RegCloseKey(key)
    except:
        print('添加失败')
    print('添加成功！')


def open_bing_url():
    print('通过bing壁纸源更新...')
    api_url = url
    api_response = open_url(api_url)
    print(api_response)
    return deal_bing(api_response)


# 根据配置获取不同的数据源
def check_img_url():
    download_url = ''
    if source == '0':
        download_url = open_bing_url()
    else:
        download_url = chrome.open_chrome_url()
    if download_url:
        download_img(download_url)
    else:
        print('图片下载链接出错')


if __name__ == '__main__':
    try:
        if check() and force_update == '0':
            print('图片已下载，路径为: ' + fullfile_name)
            refresh_desktop()
        else:
            print('网络状态 ' + str(network_state))
            while network_state != 0:
                checkNetwork()
            check_img_url()
            update_exe()
        if is_delete == '1':
            del_img()
        # 每次都将自己加入自启动
        if is_auto_run == '1':
            autoRun()
    except:
        traceback.print_exc()
