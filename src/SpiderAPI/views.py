from django.shortcuts import render
# from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime, date, time, timedelta

#from .models import Target, UserInfo, TweetsInfo, CommentWeiboInfo, CommentInfo, ImgInfo
from .models import Target,SightInfo

#from .spider import Weibo
from .spider import Ctrip

from lxml import etree
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from src.SnowNLPAPI.snownlp import SnowNLP
from src.SnowNLPAPI.snownlp import sentiment
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from collections import Counter

from os import path
import jieba
import time
import matplotlib.pyplot as plt
import base64
import json
import requests
import traceback
import re


class SpiderCtrip:
    @csrf_exempt
    def SpiderAPI(request):
        res = {}
        if request.method == "POST":
            text1 = request.POST.get("sightId")
            text2 = request.POST.get("districtId")
            page = request.POST.get("page")
            if not page:  # 默认page 为1
                page = 1
            else:
                page = int(page)  # get过来的page参数是字符串
            try:
                # UserInfo.objects.get(_id=text)
                # res['ok'] = "数据库已存在该用户，开始返回数据"
                # res['data'] = serializers.serialize("json", UserInfo.objects.filter(_id=text))
                # aritcles = TweetsInfo.objects.filter(UserInfo_id=text).order_by("-PubTime")  # 查询所有的数据
                # paginator = Paginator(aritcles, 20)  # 对数据进行分页，每页20条
                # print("=======================================")
                # print(paginator.count, paginator.num_pages)
                # pageData = paginator.page(page)
                # res['total'] = paginator.count
                # res['tweets'] = serializers.serialize("json", pageData)
                # return HttpResponse(json.dumps(res))
                SightInfo.objects.get(BusinessId=text1)
                res['ok'] = "数据库已存在该用户，开始返回数据"
                res['data'] = serializers.serialize("json", SightInfo.objects.filter(BusinessId=text1))


            except UserInfo.DoesNotExist:
                print("数据库不存在该数据，开始爬虫")
                Target.objects.filter(id=1).update(uid=text)
                resp = list(Target.objects.values('uid', 'cookie', 'add_time'))
                uid = int(resp[0]["uid"])
                cookie = {"Cookie": resp[0]["cookie"]}
                wb = Weibo(uid, cookie)
                wb.get_userInfo()
                wb.get_weibo_info()
                qqq = TweetsInfo.objects.filter(Content='').delete()
                res['ok'] = "数据库不存在该数据的爬虫"
                res['data'] = serializers.serialize("json", UserInfo.objects.filter(_id=text))
                aritcles = TweetsInfo.objects.filter(UserInfo_id=text).order_by("-PubTime")  # 查询所有的数据
                paginator = Paginator(aritcles, 20)  # 对数据进行分页，每页20条
                print("=======================================")
                print(paginator.count, paginator.num_pages)
                pageData = paginator.page(page)
                res['total'] = paginator.count
                res['tweets'] = serializers.serialize("json", pageData)
                return HttpResponse(json.dumps(res))

        # if request.method == "GET":
        #     text = request.GET.get("weiboId")

        #     print(li)
        #     return HttpResponse(json.dumps(li))


#日期转化代码
class JsonCustomEncoder(json.JSONEncoder):
    def default(self, field):
        if isinstance(field, datetime):
            return field.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(field, date):
            return field.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, field)


