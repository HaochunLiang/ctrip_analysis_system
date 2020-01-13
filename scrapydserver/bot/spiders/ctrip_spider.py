#!/usr/bin/env python
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
        title = selector.xpath('//p[@class="title"]/text()').extract()[0]
        # 特点
        tags = selector.xpath('//div[@class="tags"]/text()').extract()[1]
        # 排名
        texts = selector.xpath('//p[@class="texts"]/text()').extract()[0]
        # 评分
        commentScoreReal = selector.xpath('//p[@class="commentScoreReal"]/text()').extract()[0]
        # 评论数
        commentNumberText = selector.xpath('//p[@class="commentNumberText"]/text()').extract()[0]
        # 地方
        addressText = selector.xpath('//p[@class="addressText ellipsis"]/text()').extract()[0]
        # 到达方式
        addressWay = selector.xpath('//p[@class="addressWay"]/text()').extract()[0]
        # 图片地址
        Image = selector.xpath('//img/@src').extract()[0]
        img = []
        img.append(Image)

        sight_InfoItem = SightInfoItem()
        sight_InfoItem['BusinessId'] = response.url.split('/')[-1].split('.')[0]
        sight_InfoItem['DistrictId'] = response.url.split('/')[-2]
        sight_InfoItem['crawl_time'] = datetime.now()

        if title:
            sight_InfoItem['Title']=title
        if tags:
            sight_InfoItem['Tags'] = tags
        if texts:
            sight_InfoItem['Texts'] = texts
        if commentScoreReal:
            sight_InfoItem['CommentScoreReal'] = commentScoreReal
        if commentNumberText:
            sight_InfoItem['CommentNumberText'] = commentNumberText
        if addressText:
            sight_InfoItem['AddressText'] = addressText
        if addressWay:
            sight_InfoItem['AddressWay'] = addressWay
        if img:
            sight_InfoItem['Img'] = img

        sight_InfoItem.save()

if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl('ctrip_spider')
    process.start()
