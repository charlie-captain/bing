## 必应每日壁纸自动更换

### 前言

刚学习Python基础之后, 想写点东西来提升自己的能力.
### 使用方法
- #### 直接使用
    dist目录下的bing.exe可以直接双击使用
- #### 开机启动
    0xRefresh.xml 为windows计划任务的方案，导入之后修改bing.exe的目录路径即可；
- #### 配置文件init.ini
    - delete：0是不开启，1是开启删除非本月文件夹
    - upload: 同上，1是开启上传到bmob的(一般默认为0就好了)

### 具体实现
- #### 运行流程

    ```
    if __name__ == '__main__':
        if check():     #检查图片是否下载了
            print('图片已下载，路径为: ' + fullfile_name)
            refresh_desktop()
        else:
            print('图片不存在.')
            img_response = open_url(url)
            find_img(img_response)
        del_img()   #删除缓存图片
    ```

    然后我们一步一步地走流程
- #### check - 检查是否已经下载，初始化日期
    这里保存图片要说一下, 我是获取当前日期

    按月份做文件夹2017-10

    然后图片用完整日期2017-10-16这样.
    ```
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
    ```
- #### open_url - 网络请求
    
    就是简单的网络请求而已
    
    ```
    # connect to the url
    def open_url(url):
        request = urllib.request.Request(url)
        request.add_header('User-Agent',
                           'Mozilla/5.0 (WindowsNT 10.0; WOW64)AppleWebKit/537.36 (KHTML,like Gecko)Chrome/53.0.2785.104Safari/537.36Core/1.53.3357.400QQBrowser/9.6.11858.400')
        response =urllib.request.urlopen(request)
        return response.read()
    ```
    
- #### find_img() - 下载文件
    
    简单的文件下载处理
    ```
    # download image
    def find_img(response_html):
        print('正在下载图片...')
        jsons = json.loads(response_html)
        img_dict = jsons['images']
        img = img_dict[0]
        if img['url']:
            save_img(img['url'])
    ```

- #### save_img() - 保存文件
    

    
    然后就是一个判断,如果已经下载了就跳过,否则就下载
    ```
    # save picture
    def save_img(img_url):
        url_pic = 'http://cn.bing.com' + img_url
        img = open_url(url_pic)
        if img and not file_exist(filedir_name):
            with open(filedir_name, 'wb') as f:
                f.write(img)
            print('图片下载成功.')
            #upload_photos()    #上传到个人bmob，你们应该不需要
        else:
            print('图片已存在.')
        print('文件完整路径为:' + fullfile_name)
        refresh_desktop()  # 存不存在都要更换壁纸
    ```

- #### file_exist() - 是否已存在文件

    ```
    # find the file
    def file_exist(file_name):
        temp = os.path.exists(file_name)
        return temp
    ```
    
- #### update_img() - 更换桌面壁纸

    这里就是用来还桌面壁纸的,最重要还是用win32gui这个模块
    
    ```
    # change the destop
    def refresh_desktop():
        print('正在设置为壁纸...')
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, fullfile_name, 1 + 2)
        print('壁纸设置成功.')
    ```

- #### del_img() - 定时清空缓存
    
    删除除了这个月的其他文件夹, 也避免删除了git文件夹
    
    ```
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
    ```

    >这里删除非空文件夹用的是shutil模块,很方便
  
- #### 打包成EXE文件

    使用pyinstaller , 我用的是python3.6 可以直接使用
    
    - 安装
        
        ```
        pip install pyinstaller
        ```
        
    - 打包
        
        到需要打包的目录下打开控制台
        
        ```
        pyinstaller xxx.py
        ```

        参数如下:
        ```
        –i=图标路径
        -F 打包成一个exe文件
        -w 使用窗口，无控制台
        -c 使用控制台，无窗口
        -D 创建一个目录，里面包含exe以及其他一些依赖性文件
        pyinstaller -h 来查看参数
        ```

        默认可以使用
        
        ```
        pyinstaller -F -w -i=xx.icon  xx.py
        ```
        
- #### 计划任务实现定时更换

    这里就不详细说明了详情可以找下度娘, github已经设置好了,只是需要你们去设置下运行的路径.
    
    好了,今天就到这了

### Pull Requests

如果你有好的方法，可以参与到项目中来，因为bmob开放，所以大家可以做一个图库来获取bing的所有图片。

