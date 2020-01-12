from django.shortcuts import render
# from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime, date, time, timedelta

#from .models import Target, UserInfo, TweetsInfo, CommentWeiboInfo, CommentInfo, ImgInfo
from .models import Target,SightInfo,ImgInfo,CommentInfo

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
                SightInfo.objects.get(BusinessId=text1)
                res['ok'] = "数据库已存在该用户，开始返回数据"
                res['data'] = serializers.serialize("json", SightInfo.objects.filter(BusinessId=text1))
                aritcles = CommentInfo.objects.filter(SightInfo_id=text1)
                paginator = Paginator(aritcles, 10)  # 对数据进行分页，每页10条
                print("=======================================")
                print(paginator.count, paginator.num_pages)
                pageData = paginator.page(page)
                res['total'] = paginator.count
                res['comments'] = serializers.serialize("json", pageData)
                print("数据库已存在该用户，开始返回数据")
                return HttpResponse(json.dumps(res))

            except SightInfo.DoesNotExist:
                print("数据库不存在该数据，开始爬虫")
                Target.objects.create(sid=text1,did=text2)
                resp = list(Target.objects.values('sid','did',  'add_time'))
                print(resp)
                sid = int(resp[-1]["sid"])
                did=int(resp[-1]["did"])
                cp = Ctrip(sight_id=sid,district_id=did)
                cp.get_SightInfo()
                cp.get_CommentInfo()
                #cp.get_weibo_info()
                #qqq = TweetsInfo.objects.filter(Content='').delete()
                print("爬虫完成")
                res['ok'] = "数据库不存在该数据的爬虫"
                res['data'] = serializers.serialize("json", SightInfo.objects.filter(BusinessId=text1))
                aritcles = CommentInfo.objects.filter(SightInfo_id=text1)
                paginator = Paginator(aritcles, 10)  # 对数据进行分页，每页10条
                print("=======================================")
                print(paginator.count, paginator.num_pages)
                pageData = paginator.page(page)
                res['total'] = paginator.count
                res['comments'] = serializers.serialize("json", pageData)
                return HttpResponse(json.dumps(res))

        # if request.method == "GET":
        #     text = request.GET.get("weiboId")

        #     print(li)
        #     return HttpResponse(json.dumps(li))

    @csrf_exempt
    def WordCloudAPI(request):
        res = {}
        if request.method == "GET":
            text = request.GET.get("sightId")
            aritcles = CommentInfo.objects.filter(SightInfo_id = text)
            content = ''
            for e in aritcles:
                content += e.Content
            content = re.sub("[^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a]", "", content)
            wordlist_after_jieba = jieba.cut(content, cut_all=False)
            wl_space_split = (" ".join(wordlist_after_jieba))
            filepath = path.dirname(__file__) + '\stopword.txt'
            stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
            minganfilepath = path.dirname(__file__) + '\mingan.txt'
            minganwords = [line.strip() for line in open(minganfilepath, 'r', encoding='utf-8').readlines()]
            c=Counter()
            outstr = ''
            for word in wl_space_split:
                if word not in stopwords:
                    if word != '\t'and'\n':
                        outstr += word
            outstr = outstr.split(' ')
            while '' in outstr:
                outstr.remove('')
            for word in outstr:
                c[word] += 1
            cipin = list()
            li = list(c.items())
            li.sort(key=lambda x:x[1], reverse=True)
            mingancount = 0
            for (k, v) in li:
                if k in minganwords:
                    mingancount += 1
                cipin.append({"word":k,"count":v})
            res['mingan'] = mingancount/len(li)
            res['cipin'] = cipin
            qqq = CommentInfo.objects.filter(sentiments=0).delete()

            infos = CommentInfo.objects.filter(SightInfo_id = text).values('sentiments')
            #print(infos)
            c = Counter()
            for word in infos:
                c[word['sentiments']] += 1
            li = list(c.items())
            li.sort(key=lambda x:x[0])
            res['tu'] = json.dumps(li)
            imgInfo = ImgInfo()
            imgInfo.SightInfo_id = text
            imgInfo.wordcloud = res
            try:
                ImgInfo.objects.get(SightInfo_id = text)
                print("数据库已存在该词频")
            except ImgInfo.DoesNotExist:
                print("开始保存词频数据")
                imgInfo.save()
                print("保存词频数据成功")
        return HttpResponse(json.dumps(res))

    @csrf_exempt
    def CommentsAPI(request):
        ret = {}
        if request.method == "POST":
            text = request.POST.get("sightId")
            page = request.POST.get("page")
            print(text, page)
            if not page: #默认page 为1
                page = 1
            else:
                page = int(page) #get过来的page参数是字符串
            aritcles = CommentInfo.objects.filter(SightInfo_id = text)  #查询所有的数据
            paginator = Paginator(aritcles, 10) #对数据进行分页，每页20条
            print("=======================================")
            print(paginator.count,paginator.num_pages)
            pageData = paginator.page(page)
            ret['total'] = paginator.count
            ret['data'] = serializers.serialize("json",pageData)
            return HttpResponse(json.dumps(ret))
        if request.method == "GET":
            text = request.GET.get("sightId")
            qqq = CommentInfo.objects.filter(Content='').delete()
            all = CommentInfo.objects.filter(SightInfo_id=text)
            for e in all:
                mm = ()
                s = SnowNLP(e.Content)
                for i in s.tags:
                    mm += i
                CommentInfo.objects.filter(CommentId=e.CommentId).update(tags=s.keywords(5))
                CommentInfo.objects.filter(CommentId=e.CommentId).update(pinyin=mm)
                CommentInfo.objects.filter(CommentId=e.CommentId).update(sentiments=s.sentiments)
                print(s.keywords(5))
            return HttpResponse("success")


#日期转化代码
class JsonCustomEncoder(json.JSONEncoder):
    def default(self, field):
        if isinstance(field, datetime):
            return field.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(field, date):
            return field.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, field)


