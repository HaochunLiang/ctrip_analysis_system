import re
import requests
from urllib import request
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
from .models import Target, SightInfo,UserInfo,CommentInfo
from .agents import getAgent

class Ctrip:
    #Ctrip类初始化
    def __init__(self, sight_id,district_id, filter=0):
        self.sight_id=sight_id
        self.district_id=district_id
        #self.cookie = cookie  # 设置cookie
        self.agent = getAgent()

    #代理测试
    def getTest(self):
        print (self.agent)
        return self.agent

    #获取景点信息
    def get_SightInfo(self):
        try:
            print("正在爬虫：景点信息")
            base_url = 'https://m.ctrip.com/webapp/you/gspoi/sight/{}/{}.html'
            url=base_url.format(self.district_id,self.sight_id)
            Content_Type = 'application/x-www-form-urlencoded'
            Accept_Encoding = 'gzip, deflate'
            headers = {
                'User-Agent':self.agent['user-agent'],
                'Content-Type': Content_Type,
                'Accept-Encoding': Accept_Encoding
            }
            req = requests.get(url, headers=headers)
            soup = BeautifulSoup(req.content.decode('utf-8'), 'lxml')
            #print(soup)
            # 名字
            title = soup.find('p', {'class': 'title'}).string
            # 特点
            tags = soup.find('div', {'class': 'tags'}).contents[2]
            # 排名
            texts = soup.find('p', {'class': 'texts'}).string
            # 评分
            commentScoreReal = soup.find('p', {'class': 'commentScoreReal'}).string
            # 评论数
            commentNumberText = soup.find('p', {'class': 'commentNumberText'}).contents[0]
            # 地点
            addressText = soup.find('p', {'class': 'addressText ellipsis'}).string
            # 到达方式
            addressWay = soup.find('p', {'class': 'addressWay'}).string
            # 描述信息
            #descriptorText = soup.find('p', {'class': 'descriptorText'}).string
            #print(descriptorText)
            # 图片地址

            img=[]
            Image= soup.find('img')['src']
            img.append(Image)

            #print(img)
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
            if img:
                sightInfo.Img=img
            print("结束爬虫：景点信息")
            try:
                print(sightInfo)
                SightInfo.objects.get(BusinessId=self.sight_id)
                return "用户数据已存在！"
            except SightInfo.DoesNotExist:
                sightInfo.save()
                print("用户信息爬取成功")
                return "用户信息爬取成功!"
        except Exception as e:
            print("获取景点信息错误: ", e)
            traceback.print_exc()

    #获取每一页的评论信息,并写入数据库
    def getCommentInfoResponse(self, PageIndex):
        url = "http://m.ctrip.com/restapi/soa2/13444/json/GetCommentListAndHotTagList"
        data = {"CommentResultInfoEntity":
                    {"BusinessId": self.sight_id,
                     "BusinessType": 11,
                     "PoiId": 0,
                     "PageIndex": PageIndex,
                     "PageSize": 10,
                     "TouristType": 0,
                     "SortType": 3,
                     "ImageFilter": False,
                     "StarType": 0,
                     "CommentTagId": 0,
                     "ChannelType": 7,
                     "VideoImageWidth": 700,
                     "VideoImageHeight": 392},
                "head":
                    {"cid": "09031114111825253706",
                     "ctok": "",
                     "cver": "1.0",
                     "lang": "01",
                     "sid": "8888",
                     "syscode": "09",
                     "auth": "",
                     "extension":
                         [{"name": "protocal", "value": "https"}]},
                "contentType": "json"}

        data = json.dumps(data).encode(encoding='utf-8')
        header_dict = {'User-Agent': self.agent['user-agent'],
                       "Content-Type": "application/json"}

        url_request = request.Request(url=url, data=data, headers=header_dict)
        print("这个对象的方法是：", url_request.get_method())
        url_response = request.urlopen(url_request)
        data = url_response.read().decode('utf-8')
        dict_str = json.loads(data)
        dict_str = dict_str["CommentResult"]['CommentInfo']
        i=0
        for str in dict_str:
            i=i+1
            # 用户信息
            # 用户id
            UserId=str['UserId']
            # 用户昵称
            try:
                UserNick=str['UserInfoModel']['UserNick']
            except:
                UserNick=''
            # 用户头像
            try:
                UserImageSrc=str['UserInfoModel']['UserImageSrc']
            except:
                UserImageSrc=''
            # 用户性别
            try:
                Gender=str['UserInfoModel']['Gender']
            except:
                Gender=0
            # 用户关注数
            try:
                FriendCount=str['UserInfoModel']['FriendCount']
            except:
                FriendCount=0
            # 用户粉丝
            try:
                FollowCount=str['UserInfoModel']['FollowCount']
            except:
                FollowCount=0
            # 用户评论数
            try:
                CommentCount=str['UserInfoModel']['CommentCount']
            except:
                CommentCount=''
            # 用户地区
            try:
                UserDistrictName=str['UserInfoModel']['UserDistrictName']
            except:
                UserDistrictName=''

            # 用户信息实例化
            userInfo=UserInfo()
            userInfo.user_Id=UserId
            if UserNick:
                userInfo.user_Nick=UserNick
            if UserImageSrc:
                userInfo.user_profile_image_url=UserImageSrc
            if Gender:
                userInfo.user_Gender=Gender
            if FriendCount:
                userInfo.user_FriendCount=FriendCount
            if FollowCount:
                userInfo.user_FollowCount=FollowCount
            if CommentCount:
                userInfo.user_CommentCount=CommentCount
            if UserDistrictName:
                userInfo.user_DistrictName=UserDistrictName
            try:
                UserInfo.objects.get(user_Id=UserId)
                print("用户数据已经存在")
            except UserInfo.DoesNotExist:
                userInfo.save()
                print("用户数据存储成功")

            # 评论id
            CommentId=str['CommentId']
            # 区域id
            DistrictId=str['DistrictId']
            # 景点名字
            POIName=str['POIName']
            # 景点id
            BusinessId=str['BusinessId']
            # 用户评分
            TotalStar=str['TotalStar']
            # 评论内容
            Content=str['Content']
            # 评论时间
            AuditTime=str['AuditTime']
            # 最后修改时间
            LastModifyTime=str['LastModifyTime']
            # 评分详细
            CommentScoreList = []
            for str1 in str['CommentScoreList']:
                CommentScoreList.append(str1['Score'])

            #实例化
            commentInfo=CommentInfo()
            commentInfo.CommentId=CommentId
            if DistrictId:
                commentInfo.DistrictId=DistrictId
            if POIName:
                commentInfo.POIName=POIName
            if UserId:
                commentInfo.UserInfo_id = UserId

            commentInfo.SightInfo_id=self.sight_id
            if TotalStar:
                commentInfo.TotalStar=TotalStar
            if Content:
                commentInfo.Content=Content
                s = SnowNLP(Content)
                mm=()
                for k in s.tags:
                    mm += k
                commentInfo.tags=s.keywords(5)
                commentInfo.pinyin = mm
                print(type(s.sentiments))
                commentInfo.sentiments = s.sentiments
                #del(dict)
                #print(commentInfo.sentiments)
            if AuditTime:
                commentInfo.AuditTime=AuditTime
            if LastModifyTime:
                commentInfo.LastModifyTime=LastModifyTime
            q=1
            for qq in CommentScoreList:
                if q==1:
                    commentInfo.Score1=qq
                if q == 2:
                    commentInfo.Score2=qq
                if q==3:
                    commentInfo.Score3=qq
                q=q+1
            try:
                CommentInfo.objects.get(CommentId=CommentId)
                print("评论数据已经存在")
            except CommentInfo.DoesNotExist:
                commentInfo.save()
                print("评论数据存储成功")
        return i


    def get_CommentInfo(self):
        try:
            print("正在爬虫：评论信息")
            #分析前20
            page=1
            while page<3:
                len=self.getCommentInfoResponse(page)
                page=page+1
                if len<10:
                    break
            print("结束爬虫：评论信息")
        except Exception as e:
            print("Error评论信息: ", e)
            traceback.print_exc()

