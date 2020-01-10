import re
import requests
import traceback
import sys
import random
import time
import js2xml
import json
import urllib
import os

from os import path
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
from lxml import etree
from src.SnowNLPAPI.snownlp import SnowNLP
from src.SnowNLPAPI.snownlp import sentiment
from .models import Target, SightInfo
from .agents import getAgent

class Ctrip:
    #Ctrip类初始化
    def __init__(self, sight_id,district_id, cookie, filter=0):
        self.sight_id=sight_id
        self.district_id=district_id
        self.cookie = cookie  # 设置cookie
        self.agent = getAgent()

    #代理测试
    def getTest(self):
        print (self.agent)
        return self.agent

    #获取景点信息
    def get_SightInfo(self):
        try:
            base_url = 'https://m.ctrip.com/webapp/you/gspoi/sight/{}/{}.html'
            url=base_url.format(self.district_id,self.sight_id)
            Content_Type = 'application/x-www-form-urlencoded'
            Accept_Encoding = 'gzip, deflate'
            headers = {
                'User-Agent':self.agent['user-agent'],
                'Cookie': self.cookie,
                'Content-Type': Content_Type,
                'Accept-Encoding': Accept_Encoding
            }
            req = requests.get(url, headers=headers)
            soup = BeautifulSoup(req.content.decode('utf-8'), 'lxml')
            # 名字
            title = soup.find('p', {'class': 'title'})
            # 特点
            tags = soup.find('div', {'class': 'tags'})
            # 排名
            texts = soup.find('p', {'class': 'texts'})
            # 评分
            commentScoreReal = soup.find('p', {'class': 'commentScoreReal'})
            # 评论数
            commentNumberText = soup.find('p', {'class': 'commentNumberText'})
            # 地点
            addressText = soup.find('p', {'class': 'addressText ellipsis'})
            # 到达方式
            addressWay = soup.find('p', {'class': 'addressWay'})
            # 描述信息
            descriptorText = soup.find('p', {'class': 'descriptorText'})
            # 图片地址
            img = soup.find('img')['src']

            #实例化
            sightInfo=SightInfo()
            sightInfo.BusinessId=self.sight_id
            sightInfo.DistrictId=self.district_id

            if title:
                sightInfo.Title=title
            if tags:
                sightInfo.Tags=tags
            if texts:
                sightInfo.Texts=texts
            if commentScoreReal:
                sightInfo.CommentScoreReal=commentScoreReal
            if commentNumberText:
                sightInfo.CommentNumberText=commentNumberText
            if addressText:
                sightInfo.AddressText=addressText
            if addressWay:
                sightInfo.AddressWay=addressWay
            if descriptorText:
                sightInfo.DescriptorText=descriptorText
            if img:
                sightInfo.Img=img
            try:
                sightInfo.objects.get(BusinessId= self.sight_id)
            except sightInfo.DoesNotExist:
                sightInfo.save()
                return "用户信息爬取成功~"
        except Exception as e:
            print("获取景点信息错误: ", e)
            traceback.print_exc()