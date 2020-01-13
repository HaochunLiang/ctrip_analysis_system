# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy_djangoitem import DjangoItem

#from src.ScrapydAPI.models import SightInfo
from ScrapydAPI.models import Target,SightInfo,UserInfo,CommentInfo

class TargetItem(DjangoItem):
    django_model = Target

class SightInfoItem(DjangoItem):
    django_model = SightInfo

class UserInfoItem(DjangoItem):
    django_model = UserInfo

class CommentInfoItem(DjangoItem):
    django_model = CommentInfo
