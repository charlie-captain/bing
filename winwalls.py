# -*- coding: utf-8 -*-
# get photos from win10 screen_lock
from PIL import Image
import os, shutil
import getpass
import time

src = "C:\\Users\\" + getpass.getuser() + "\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets\\"
image_list = os.listdir(src)
new_src = "C:\\Users\\" + getpass.getuser() + "\\Pictures"


def get_photos():
    i = 1
    for img in image_list:
        img_path = os.path.join(src, img)
        os.rename(img_path, img_path + ".jpg")
        img = Image.open(img_path + ".jpg")
        w, h = img.size
        if w < 1920 or h > 1920:
            continue
        os.rename(img_path+".jpg",img_path)
        img_name = time.strftime("%Y-%m-%d", time.localtime()) + "-" + str(i) + ".jpg"
        new_img_path = os.path.join(new_src, img_name)
        shutil.copyfile(img_path + ".jpg", new_img_path)
        i += 1

