#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd7in5b
import time
import datetime
import os
import requests
import json
import urllib.error
import urllib.request
from PIL import Image,ImageDraw,ImageFont
import traceback

def download_image(url, dst_path):
    try:
        data = urllib.request.urlopen(url).read()
        with open(dst_path, mode="wb") as f:
            f.write(data)
    except urllib.error.URLError as e:
        print(e)

try:
    epd = epd7in5b.EPD()
    epd.init()
    # print("Clear...")
    # epd.Clear(0xFF)
    fontType = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
    apikey = "ここにTMDBのAPIkeyを入力"
    media_type = "movie"
    time_window = "day"
    api = "https://api.themoviedb.org/3/trending/{mediaType}/{timeWindow}?api_key={key}"
    url = api.format(mediaType=media_type, timeWindow=time_window,key=apikey)
    r = requests.get(url)
    data = json.loads(r.text)
    HRedimage = Image.new('1', (epd7in5b.EPD_HEIGHT, epd7in5b.EPD_WIDTH), 255)  # 298*126    
    font24 = ImageFont.truetype(fontType, 20)
    drawred = ImageDraw.Draw(HRedimage)
    minute = int(time.strftime("%M"))
    drawred.text((10,10),u"海外映画時報　"+time.strftime('%m/%d %H:%M')+u"更新",font = font24, fill = 0)
    str1 = str(int(minute/3)+1)+u"位："+data["results"][int(minute/3)]["title"]
    drawred.text((10,40),str1,font = font24, fill = 0)
    str2 = u"人気："+str(int(data["results"][int(minute/3)]["popularity"]))
    drawred.text((10,70),str2,font = font24,fill = 0)
    str3 = u"評価："+str(int(data["results"][int(minute/3)]["vote_average"]))+"/10"
    drawred.text((10,100),str3,font = font24, fill = 0)
    str4 = u"公開："+str(data["results"][int(minute/3)]["release_date"])
    drawred.text((10,130),str4,font = font24, fill = 0)
    imgUrl = "https://image.tmdb.org/t/p/w500"+data["results"][int(minute/3)]["poster_path"]
    dst_path = os.path.dirname(os.path.abspath(__file__))+"/images/image.jpg"
    download_image(imgUrl, dst_path)
    im = Image.open(os.path.dirname(os.path.abspath(__file__))+"/images/image.jpg")
    im_rotate = im.rotate(90, expand = True)
    gray_img = im_rotate.convert('L')
    img_resize = gray_img.resize((640,384))
    img_resize.save(os.path.dirname(os.path.abspath(__file__))+"/images/image.bmp")
    HBlackimage = Image.open(os.path.dirname(os.path.abspath(__file__))+"/images/image.bmp")
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRedimage))

    epd.sleep()
        
except:
    print('traceback.format_exc():\n%s',traceback.format_exc())
    exit()


