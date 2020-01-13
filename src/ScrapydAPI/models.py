from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
# -*- utf-8 -*-
from datetime import datetime

from django.db import models

# Create your models here.
class Target(models.Model):
    sid = models.CharField(max_length=20, verbose_name=u"爬取景点id")
    did = models.CharField(max_length=20, verbose_name=u"景点地区id")
    isScrapy = models.IntegerField(default=0, verbose_name=u"是否爬取")
    cookie = models.TextField(verbose_name=u"设置cookie",  blank=True)
    group = models.IntegerField(default=0, verbose_name=u"景点分组")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"爬虫设置"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}".format(self.sid)

class SightInfo(models.Model):
    # 名字
    Title =models.CharField(max_length=50, verbose_name=u"名字", blank=True)
    # 景点id
    BusinessId=models.IntegerField(default=0, verbose_name=u'景点id', primary_key=True)
    #地区id
    DistrictId=models.IntegerField(default=0, verbose_name=u'地区id')
    # 特点
    Tags = models.CharField(max_length=30, verbose_name=u"特点", blank=True)
    # 排名
    Texts = models.CharField(max_length=30, verbose_name=u"排名", blank=True)
    # 评分
    CommentScoreReal=models.CharField(max_length=3, verbose_name=u"评分", blank=True)
    # 评论数
    CommentNumberText =models.IntegerField(default=0, verbose_name=u'评论数', blank=True)
    # 地点
    AddressText = models.CharField(max_length=30, verbose_name=u"地点", blank=True)
    # 到达方式
    AddressWay= models.CharField(max_length=50, verbose_name=u"到达方式", blank=True)
    # 描述信息
    #DescriptorText= models.TextField(verbose_name=u"描述信息", blank=True)
    # 图片地址
    Img = models.TextField(verbose_name=u"图片地址", blank=True)
    #抓取时间
    crawl_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"景点信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}".format(self.Title)


class UserInfo(models.Model):
    #评论用户信息
    user_Id = models.CharField(max_length=50, verbose_name=u"用户的ID", primary_key=True)
    user_Nick = models.CharField(max_length=50, verbose_name=u"用户的昵称", blank=True)
    user_profile_image_url = models.TextField(verbose_name=u"用户的头像", blank=True)
    user_Gender = models.IntegerField(default=0, verbose_name=u'用户性别', blank=True)
    user_FriendCount=models.IntegerField(default=0, verbose_name=u'用户关注数', blank=True)
    user_FollowCount=models.IntegerField(default=0, verbose_name=u'用户粉丝', blank=True)
    user_CommentCount=models.IntegerField(default=0, verbose_name=u'用户评论数', blank=True)
    user_DistrictName=models.CharField(max_length=50, verbose_name=u"用户地区", blank=True)
    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name
    def __str__(self):
        return "{0}".format(self.user_Nick)

class CommentInfo(models.Model):
    #景点评论信息
    UserInfo = models.ForeignKey(UserInfo, verbose_name=u"评论用户信息", on_delete=models.CASCADE)
    SightInfo= models.ForeignKey(SightInfo, verbose_name=u"景点信息", on_delete=models.CASCADE)
    CommentId = models.CharField(max_length=50, verbose_name=u"评论的ID", primary_key=True)
    DistrictId= models.CharField(max_length=50, verbose_name=u"区域的ID", blank=True)
    POIName = models.CharField(max_length=50, verbose_name=u"景点名字", blank=True)
    TotalStar = models.CharField(max_length=3, verbose_name=u"用户评分", blank=True)
    Content=models.TextField(verbose_name=u"评论内容", blank=True)
    AuditTime=models.CharField(max_length=50, verbose_name=u"评论时间", blank=True)
    LastModifyTime=models.CharField(max_length=50, verbose_name=u"最后修改时间", blank=True)
    Score1 = models.CharField(max_length=3, verbose_name=u"景色评分", blank=True)
    Score2 = models.CharField(max_length=3, verbose_name=u"趣味评分", blank=True)
    Score3 = models.CharField(max_length=3, verbose_name=u"性价比评分", blank=True)

    #tags = models.TextField(verbose_name=u"标签", blank=True)
    #pinyin = models.TextField(verbose_name=u"词性", blank=True)
    #sentiments = models.FloatField(default=0, verbose_name=u"情感值", blank=True)
    crawl_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间", blank=True)

    class Meta:
        verbose_name = u"评论详情"
        verbose_name_plural = verbose_name
    def __str__(self):
        return "{0}".format(self.UserInfo)
