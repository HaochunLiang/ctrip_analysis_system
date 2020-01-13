#!/usrPageIndex=Nonen
# encoding: utf-8
import re
from lxml import etree
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
from bot.items import TargetItem,SightInfoItem,UserInfoItem,CommentInfoItem
from bot.spiders.utils import time_fix
from datetime import datetime
import  json
from urllib import request
import traceback
from bs4 import BeautifulSoup
import pymysql.cursors

class CtripSpider(Spider):
    name = "ctrip_spider"
    base_url = "https://m.ctrip.com"

    def start_requests(self):
        import pymysql.cursors
        # 连接数据库
        connect = pymysql.connect(
            host='localhost',  # 数据库地址
            port=3306,  # 数据库端口
            db='CtripAnalysisSystem',  # 数据库名
            user='root',  # 数据库用户名
            passwd='root',  # 数据库密码
            charset='utf8mb4',  # 编码方式
            use_unicode=True)
        # 通过cursor执行增删查改
        cursor = connect.cursor()
        cursor.execute("""SELECT sid,did from scrapydapi_target WHERE isScrapy=0""")
        sids = cursor.fetchall()
        start_sids = sids
        print('sid:::',sids)
        for sid in start_sids:
            cursor.execute("""UPDATE scrapydapi_target set isScrapy=1 WHERE sid=%s""" % sid[0])
            cursor.execute("commit")
            yield Request(url="https://m.ctrip.com/webapp/you/gspoi/sight/%s/%s.html" % (sid[1],sid[0]), callback=self.parse_information)
        connect.close()
        cursor.close()

    def parse_information(self, response):
        sight_InfoItem=SightInfoItem()
        sight_InfoItem['crawl_time']=datetime.now()
        selector = Selector(response)
        # 名字
        title = selector.xpath('//p[@class="title"]/text()').extract()
        if title and title[0]:
            sight_InfoItem['Title'] = title[0]
        # 特点
        tags = selector.xpath('//div[@class="tags"]/text()').extract()
        if tags and tags[1]:
            sight_InfoItem['Tags'] = tags[1]
        # 排名
        texts = selector.xpath('//p[@class="texts"]/text()').extract()
        if texts and texts[0]:
            sight_InfoItem['Texts'] = texts[0]
        # 评分
        commentScoreReal = selector.xpath('//p[@class="commentScoreReal"]/text()').extract()
        if commentScoreReal and commentScoreReal[0]:
            sight_InfoItem['CommentScoreReal'] = commentScoreReal[0]
        # 评论数
        commentNumberText = selector.xpath('//p[@class="commentNumberText"]/text()').extract()
        if commentNumberText and commentNumberText[0]:
            sight_InfoItem['CommentNumberText'] = commentNumberText[0]
        # 地方
        addressText = selector.xpath('//p[@class="addressText ellipsis"]/text()').extract()
        if addressText and addressText[0]:
            sight_InfoItem['AddressText'] = addressText[0]
        else:
            sight_InfoItem['AddressText']=''
        # 到达方式
        addressWay = selector.xpath('//p[@class="addressWay"]/text()').extract()
        if addressWay and addressWay[0]:
            sight_InfoItem['AddressWay'] = addressWay[0]
        #描述信息
        descriptorText=selector.xpath('//p[@class="descriptorText"]/text()').extract()
        if descriptorText and descriptorText[0]:
            sight_InfoItem['DescriptorText']=descriptorText[0]
        #开放时间
        openTimeText=selector.xpath('//p[@class="openTimeText"]/text()').extract()
        if openTimeText and openTimeText[0]:
            sight_InfoItem['OpenTimeSubText']=openTimeText[0]
        # 图片地址
        Image = selector.xpath('//img/@src').extract()
        img = []
        if Image and Image[0]:
            img.append(Image[0])
        sight_InfoItem['Img'] = img

        #sight_InfoItem = SightInfoItem()
        sight_InfoItem['BusinessId'] = response.url.split('/')[-1].split('.')[0]
        sight_InfoItem['DistrictId'] = response.url.split('/')[-2]
        sight_InfoItem['crawl_time'] = datetime.now()
        #sight_InfoItem.save()

        # 爬取评论和用户信息
        #get_CommentInfo(sid=sight_InfoItem['BusinessId'])
        yield sight_InfoItem
        sid=sight_InfoItem['BusinessId']
        postUrl = "http://m.ctrip.com/restapi/soa2/13444/json/GetCommentListAndHotTagList"
        data=self.get_Body(sid=sid,PageIndex=1)
        yield Request(
            postUrl,
            body=json.dumps(data).encode(encoding='utf-8'),
            method='POST',
            headers={'Content-Type': 'application/json'},
            callback=lambda response, sid=sid, PageIndex=1: self.get_CommentInfo(response,sid,PageIndex))


    def get_CommentInfo(self,response,sid,PageIndex):
        postUrl = "http://m.ctrip.com/restapi/soa2/13444/json/GetCommentListAndHotTagList"
        jsonArray = json.loads(response.body)["CommentResult"]['CommentInfo']
        #存成json格式
        #with open('data.json', 'w') as fw:
        #    json.dump(jsonArray, fw)
        i = 0
        for str in jsonArray:
            i = i + 1
            # 用户信息
            # 用户id
            UserId = str['UserId']

            UserInfoModel = json.dumps(str['UserInfoModel'])
            UserInfoModel = json.loads(UserInfoModel)
            if UserInfoModel is not None:
                # 用户昵称
                UserNick = str['UserInfoModel']['UserNick']
                # 用户头像
                UserImageSrc = str['UserInfoModel']['UserImageSrc']
                # 用户性别
                Gender = str['UserInfoModel']['Gender']
                # 用户关注数
                FriendCount = str['UserInfoModel']['FriendCount']
                # 用户粉丝
                FollowCount = str['UserInfoModel']['FollowCount']
                # 用户评论数
                CommentCount = str['UserInfoModel']['CommentCount']
                # 用户地区
                UserDistrictName = str['UserInfoModel']['UserDistrictName']
            else:
                UserNick = ''
                UserImageSrc = ''
                Gender = 0
                FriendCount = 0
                FollowCount = 0
                CommentCount = 0
                UserDistrictName = ''
            # 用户信息实例化
            user_InfoItem = UserInfoItem()
            user_InfoItem['user_Id'] = UserId
            if UserNick:
                user_InfoItem['user_Nick'] = UserNick
            if UserImageSrc:
                user_InfoItem['user_profile_image_url'] = UserImageSrc
            if Gender:
                user_InfoItem['user_Gender'] = Gender
            if FriendCount:
                user_InfoItem['user_FriendCount'] = FriendCount
            if FollowCount:
                user_InfoItem['user_FollowCount'] = FollowCount
            if CommentCount:
                user_InfoItem['user_CommentCount'] = CommentCount
            if UserDistrictName:
                user_InfoItem['user_DistrictName'] = UserDistrictName
            # user_InfoItem.objects.filter(user_Id=UserId):
            # list_user=user_InfoItem.objects.filter(user_Id=UserId)
            # if list_user:
            #     yield user_InfoItem

            try:
                user_InfoItem.objects.get(user_Id=UserId)
                print("用户数据已经存在")
            except:
                yield user_InfoItem
                #user_InfoItem.save()
                print("用户数据存储成功")

            # 评论id
            CommentId = str['CommentId']
            # 区域id
            DistrictId = str['DistrictId']
            # 景点名字
            POIName = str['POIName']
            # 景点id
            BusinessId = str['BusinessId']
            # 用户评分
            TotalStar = str['TotalStar']
            # 评论内容
            Content = str['Content']
            # 评论时间
            AuditTime = str['AuditTime']
            # 最后修改时间
            LastModifyTime = str['LastModifyTime']
            # 评分详细
            CommentScoreList = []
            for str1 in str['CommentScoreList']:
                CommentScoreList.append(str1['Score'])

            # 实例化
            comment_InfoItem = CommentInfoItem()
            comment_InfoItem['CommentId'] = CommentId
            if DistrictId:
                comment_InfoItem['DistrictId'] = DistrictId
            if POIName:
                comment_InfoItem['POIName'] = POIName
            if UserId:
                comment_InfoItem['UserInfo_id'] = UserId

            comment_InfoItem['SightInfo_id'] = sid
            if TotalStar:
                comment_InfoItem['TotalStar'] = TotalStar
            if Content:
                comment_InfoItem['Content'] = Content

                # del(dict)
                # print(commentInfo.sentiments)
            if AuditTime:
                comment_InfoItem['AuditTime'] = AuditTime
            if LastModifyTime:
                comment_InfoItem['LastModifyTime'] = LastModifyTime
            q = 1
            for qq in CommentScoreList:
                if q == 1:
                    comment_InfoItem['Score1'] = qq
                if q == 2:
                    comment_InfoItem['Score2'] = qq
                if q == 3:
                    comment_InfoItem['Score3'] = qq
                q = q + 1

            # list_comment=comment_InfoItem.objects.filter(CommentId=CommentId)
            # if list_comment:
            #     yield comment_InfoItem
            try:
                comment_InfoItem.objects.get(CommentId=CommentId)
                print("评论数据已经存在")
            except:
                #comment_InfoItem.save()
                yield comment_InfoItem
                print("评论数据存储成功")
        if i==10:
            data = self.get_Body(sid=sid, PageIndex=PageIndex+1)
            yield Request(
                postUrl,
                body=json.dumps(data).encode(encoding='utf-8'),
                method='POST',
                headers={'Content-Type': 'application/json'},
                callback=lambda response, sid=sid, PageIndex=PageIndex+1: self.get_CommentInfo(response, sid, PageIndex))



    def get_Body(self,sid,PageIndex):
        data = {"CommentResultInfoEntity":
                    {"BusinessId": sid,
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
        return data





def getCommentInfoResponse(sid, PageIndex):
    url = "http://m.ctrip.com/restapi/soa2/13444/json/GetCommentListAndHotTagList"
    data = {"CommentResultInfoEntity":
                {"BusinessId": sid,
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
    header_dict = {'User-Agent': "Mozilla/5.0 (Linux; U; Android 0.5; en-us) AppleWebKit/522  (KHTML, like Gecko) Safari/419.3",
                   "Content-Type": "application/json"}

    url_request = request.Request(url=url, data=data, headers=header_dict)
    print("这个对象的方法是：", url_request.get_method())
    url_response = request.urlopen(url_request)
    data = url_response.read().decode('utf-8')
    dict_str = json.loads(data)
    dict_str = dict_str["CommentResult"]['CommentInfo']
    i = 0
    for str in dict_str:
        i = i + 1
        # 用户信息
        # 用户id
        UserId = str['UserId']

        UserInfoModel=json.dumps(str['UserInfoModel'])
        UserInfoModel=json.loads(UserInfoModel)
        if UserInfoModel is not None:
            # 用户昵称
            UserNick = str['UserInfoModel']['UserNick']
            # 用户头像
            UserImageSrc = str['UserInfoModel']['UserImageSrc']
            # 用户性别
            Gender = str['UserInfoModel']['Gender']
            # 用户关注数
            FriendCount = str['UserInfoModel']['FriendCount']
            # 用户粉丝
            FollowCount = str['UserInfoModel']['FollowCount']
            # 用户评论数
            CommentCount = str['UserInfoModel']['CommentCount']
            # 用户地区
            UserDistrictName = str['UserInfoModel']['UserDistrictName']
        else:
            UserNick=''
            UserImageSrc=''
            Gender=0
            FriendCount=0
            FollowCount=0
            CommentCount=0
            UserDistrictName=''
        # 用户信息实例化
        user_InfoItem = UserInfoItem()
        user_InfoItem['user_Id']  = UserId
        if UserNick:
            user_InfoItem['user_Nick'] = UserNick
        if UserImageSrc:
            user_InfoItem['user_profile_image_url'] = UserImageSrc
        if Gender:
            user_InfoItem['user_Gender'] = Gender
        if FriendCount:
            user_InfoItem['user_FriendCount'] = FriendCount
        if FollowCount:
            user_InfoItem['user_FollowCount'] = FollowCount
        if CommentCount:
            user_InfoItem['user_CommentCount'] = CommentCount
        if UserDistrictName:
            user_InfoItem['user_DistrictName'] = UserDistrictName
        #user_InfoItem.objects.filter(user_Id=UserId):
        try:
            user_InfoItem.objects.get(user_Id=UserId)
            print("用户数据已经存在")
        except:
            #yield user_InfoItem
            user_InfoItem.save()
            print("用户数据存储成功")

        # 评论id
        CommentId = str['CommentId']
        # 区域id
        DistrictId = str['DistrictId']
        # 景点名字
        POIName = str['POIName']
        # 景点id
        BusinessId = str['BusinessId']
        # 用户评分
        TotalStar = str['TotalStar']
        # 评论内容
        Content = str['Content']
        # 评论时间
        AuditTime = str['AuditTime']
        # 最后修改时间
        LastModifyTime = str['LastModifyTime']
        # 评分详细
        CommentScoreList = []
        for str1 in str['CommentScoreList']:
            CommentScoreList.append(str1['Score'])

        # 实例化
        comment_InfoItem = CommentInfoItem()
        comment_InfoItem['CommentId'] = CommentId
        if DistrictId:
            comment_InfoItem['DistrictId'] = DistrictId
        if POIName:
            comment_InfoItem['POIName'] = POIName
        if UserId:
            comment_InfoItem['UserInfo_id'] = UserId

        comment_InfoItem['SightInfo_id'] = sid
        if TotalStar:
            comment_InfoItem['TotalStar'] = TotalStar
        if Content:
            comment_InfoItem['Content'] = Content

            # del(dict)
            # print(commentInfo.sentiments)
        if AuditTime:
            comment_InfoItem['AuditTime'] = AuditTime
        if LastModifyTime:
            comment_InfoItem['LastModifyTime'] = LastModifyTime
        q = 1
        for qq in CommentScoreList:
            if q == 1:
                comment_InfoItem['Score1'] = qq
            if q == 2:
                comment_InfoItem['Score2'] = qq
            if q == 3:
                comment_InfoItem['Score3'] = qq
            q = q + 1

        try:
            comment_InfoItem.objects.get(CommentId=CommentId)
            print("评论数据已经存在")
        except:
            comment_InfoItem.save()
            #yield comment_InfoItem
            print("评论数据存储成功")
    return i


def get_CommentInfo(sid):
    try:
        print("正在爬虫：评论信息")
        #分析前20
        page=1
        while True:
            len=getCommentInfoResponse(sid=sid,PageIndex=page)
            page=page+1
            if int(len)<10:
                break
        print("结束爬虫：评论信息")
    except Exception as e:
        print("Error评论信息: ", e)
        traceback.print_exc()

if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl('ctrip_spider')
    process.start()
