import xadmin
from xadmin import views

from .models import Target,SightInfo,UserInfo,CommentInfo,ImgInfo


class TargetAdmin(object):
  list_display = ['sid','did', 'add_time']
  search_fields = ['sid', 'did', 'add_time']
  list_filter = ['sid','did', 'add_time']

class SightInfoAdmin(object):
    list_display = ['Title', 'BusinessId', 'DistrictId','Tags','Texts','CommentScoreReal','CommentNumberText','AddressText','AddressWay','Img']
    search_fields =['Title', 'BusinessId', 'DistrictId','Tags','Texts','CommentScoreReal','CommentNumberText','AddressText','AddressWay','Img']
    list_filter =['Title', 'BusinessId', 'DistrictId','Tags','Texts','CommentScoreReal','CommentNumberText','AddressText','AddressWay','Img']

class UserInfoAdmin(object):
    list_display = ['user_Id', 'user_Nick', 'user_profile_image_url', 'user_Gender','user_FriendCount','user_FollowCount','user_CommentCount','user_DistrictName']
    search_fields = ['user_Id', 'user_Nick', 'user_profile_image_url', 'user_Gender','user_FriendCount','user_FollowCount','user_CommentCount','user_DistrictName']
    list_filter = ['user_Id', 'user_Nick', 'user_profile_image_url', 'user_Gender','user_FriendCount','user_FollowCount','user_CommentCount','user_DistrictName']

class CommentInfoAdmin(object):
    list_display = ['UserInfo','POIName','TotalStar','Content','tags','pinyin','sentiments']
    search_fields = ['UserInfo_user_Nick', 'SightInfo', 'CommentId', 'DistrictId','POIName','TotalStar','Content','AuditTime','LastModifyTime','Score1','Score2','Score3','tags','pinyin','sentiments','crawl_time']
    list_filter =  ['UserInfo', 'SightInfo', 'CommentId', 'DistrictId','POIName','TotalStar','Content','AuditTime','LastModifyTime','Score1','Score2','Score3','tags','pinyin','sentiments','crawl_time']

class ImgInfoAdmin(object):
    list_display = ['SightInfo', 'wordcloud']
    search_fields =  ['SightInfo_Title', 'wordcloud']
    list_filter = ['SightInfo', 'wordcloud']


class BaseSetting(object):
  enable_themes = True
  use_bootswatch = True


class GlobalSettings(object):
  site_title = u"携程旅行情感分析系统后台"
  site_footer = u"携程旅行情感分析系统"
  menu_style = "accordion"


xadmin.site.register(Target, TargetAdmin)
xadmin.site.register(SightInfo, SightInfoAdmin)
xadmin.site.register(UserInfo, UserInfoAdmin)
xadmin.site.register(CommentInfo, CommentInfoAdmin)
xadmin.site.register(ImgInfo, ImgInfoAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)