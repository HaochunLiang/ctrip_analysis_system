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
            ctripinfos = CommentInfo.objects.filter(SightInfo_id=text)
            if ctripinfos.count()!=0:
                print("数据库已存在该景点，开始返回数据")
                res['ok'] = "数据库已存在该景点，开始返回数据"
                #ctripinfos=CommentInfo.objects.filter(SightInfo_id=text)
                print(ctripinfos.count())
                #对数据进行去重
                ctripinfos=ctripinfos.values('Content').distinct()
                print(ctripinfos.count())
                #print(ctripinfos)
                #统计词频
                c = Counter()
                outstr = ''
                # 去除停用词
                filepath = path.dirname(__file__) + '\stopword.txt'
                stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
                print(stopwords)
                print(type(stopwords[-1]))
                #  stopwords2=['&','#','A','x','F','�','【','】','✌','✨']
                for ctripinfo in ctripinfos:
                    print(ctripinfo['Content'])
                    #print(type(ctripinfo['Content']))
                    wordlist_after_jieba = jieba.cut(ctripinfo['Content'], cut_all=False)
                    wl_space_split = (" ".join(wordlist_after_jieba))
                    # #去除停用词
                    # filepath = path.dirname(__file__) + '\stopword.txt'
                    # stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
                    # print()
                    #print(wl_space_split)
                    #print(type(wl_space_split))
                    #print(type(wl_space_split[0]))
                    for word in wl_space_split:
                        if word not in stopwords:
                            if word != '\t' and '\n':
                                #if word not in stopwords2:
                               outstr += word
                    break
                #print(outstr)
                outstr = outstr.split(' ')

                while '' in outstr:
                    outstr.remove('')
                    #break#
                #print(outstr)
                for word in outstr:
                    c[word] += 1
                print(outstr)
                cipin = list()
                li = list(c.items())
                li.sort(key=lambda x: x[1], reverse=True)
                #mingancount = 0
                for (k, v) in li:
                    cipin.append({"word": k, "count": v})
                print(cipin)
            else:
                print("数据库不存在该评论，正在爬虫生成")
                print(text)
                print("555555")

            return HttpResponse(None)