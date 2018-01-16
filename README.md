## 必应每日壁纸自动更换

### 前言

刚学习Python基础之后, 想写点东西来提升自己的能力.

- #### 运行流程

    ```
    url = 'http://cn.bing.com/HPImageArchive.asp?format=js&idx=0&n=1'
    img_response = open_url(url)
    find_img(img_response)
    del_img()
    ```

    然后我们一步一步地走流程
    
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
    
    这里保存图片要说一下, 我是获取当前日期

    按月份做文件夹2017-10
    
    然后图片用完整日期2017-10-16这样.
    
    然后就是一个判断,如果已经下载了就跳过,否则就下载
    ```
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
    def update_img(file_name):
        dir_name = os.path.abspath('.')
        print(dir_name)
        img_path = os.path.join(dir_name, file_name)
        print(img_path)
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, img_path, 1 + 2)
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
        –icon=图标路径
        -F 打包成一个exe文件
        -w 使用窗口，无控制台
        -c 使用控制台，无窗口
        -D 创建一个目录，里面包含exe以及其他一些依赖性文件
        pyinstaller -h 来查看参数
        ```
        
        默认可以使用
        
        ```
        pyinstaller -F -w -icon=xx.icon  xx.py
        ```
        
- #### 计划任务实现定时更换

    这里就不详细说明了详情可以找下度娘, github已经设置好了,只是需要你们去设置下运行的路径.
    
    好了,今天就到这了
    
### Github
- [https://github.com/thatnight/bing](https://github.com/thatnight/bing)
    
