from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from .models import Target, UserInfo, SightInfo,CommentInfo
from collections import Counter
from src.SnowNLPAPI.snownlp import SnowNLP
from src.SnowNLPAPI.snownlp import sentiment
from os import path
# Create your views here.
import requests
import json
import re
import jieba

class ScrapydCtrip:
    @csrf_exempt
    def ScrapydAPI(request):
        if request.method == "POST":
            ids = request.POST.get("sightIds").split(';')
            cookies = request.POST.get("cookies")
            #cookies=""
            #ids="9216,155;1837733,155"
            #ids=ids.split(';')
            target_list_to_insert = list()
            for id in ids:
                target = Target()
                print(id)
                id1=id.split(',')
                print(id1)
                #print(id1[1])
                target.sid = id1[0]
                target.did = id1[1]
                target.cookie = cookies
                try:
                    Target.objects.filter(isScrapy=0).update(cookie=cookies)
                    Target.objects.get(sid = target.sid)
                    print("该用户已存在数据库")
                except Target.DoesNotExist:
                    target_list_to_insert.append(target)
            Target.objects.bulk_create(target_list_to_insert)
            #print(ids,cookies)
            url = 'http://localhost:6800/schedule.json'
            data = {'project':'bot', 'spider':'ctrip_spider'}
            schedule = requests.post(url=url,data=data)
            return HttpResponse(schedule)
        if request.method == "GET":
            requrl = "http://localhost:6800/daemonstatus.json"
            result = requests.get(requrl)
            return HttpResponse(result)

    @csrf_exempt
    def getComment(request):
        res={}
        if request.method == "POST":
            text = request.POST.get("commentId")
            print(text)
            print(type(text))
            #try:
            #CommentInfo.objects.filter(SightInfo_id=text)
            ctripinfos = CommentInfo.objects.filter(SightInfo_id=text)

            res['ok'] = "数据库已存在该景点，开始返回数据"
            #ctripinfos=CommentInfo.objects.filter(SightInfo_id=text)
            print(ctripinfos.count())
            #对数据进行去重
            ctripinfos=ctripinfos.values('Content').distinct()
            print(ctripinfos.count())
            print(ctripinfos)
            for ctripinfo in ctripinfos:
                print(ctripinfo['Content'])
                print(type(ctripinfo['Content']))
                break
            #except:
                #print("数据库不存在该评论，正在爬虫生成")
                #print(text)
                #print("555555")

            return HttpResponse(None)