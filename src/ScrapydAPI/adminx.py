import xadmin

from xadmin import views
# here put the import lib
from .models import Target, UserInfo,CommentInfo,SightInfo


class TargetAdmin(object):
  list_display = ['sid','did','cookie', 'isScrapy', 'group','add_time']
  search_fields = ['sid', 'did','cookie', 'isScrapy','group', 'add_time']
  list_filter = ['sid','did','cookie', 'isScrapy', 'group','add_time']

class SightInfoAdmin(object):
    list_display = ['Title', 'BusinessId', 'DistrictId','Tags','Texts','CommentScoreReal','CommentNumberText','AddressText','AddressWay','Img','crawl_time']
    search_fields =['Title', 'BusinessId', 'DistrictId','Tags','Texts','CommentScoreReal','CommentNumberText','AddressText','AddressWay','Img','crawl_time']
    list_filter =['Title', 'BusinessId', 'DistrictId','Tags','Texts','CommentScoreReal','CommentNumberText','AddressText','AddressWay','Img','crawl_time']

class UserInfoAdmin(object):
    list_display = ['user_Id', 'user_Nick', 'user_profile_image_url', 'user_Gender','user_FriendCount','user_FollowCount','user_CommentCount','user_DistrictName']
    search_fields = ['user_Id', 'user_Nick', 'user_profile_image_url', 'user_Gender','user_FriendCount','user_FollowCount','user_CommentCount','user_DistrictName']
    list_filter = ['user_Id', 'user_Nick', 'user_profile_image_url', 'user_Gender','user_FriendCount','user_FollowCount','user_CommentCount','user_DistrictName']

class CommentInfoAdmin(object):
    list_display = ['UserInfo','POIName','TotalStar','Content']
    search_fields = ['UserInfo_user_Nick', 'SightInfo', 'CommentId', 'DistrictId','POIName','TotalStar','Content','AuditTime','LastModifyTime','Score1','Score2','Score3','crawl_time']
    list_filter =  ['UserInfo', 'SightInfo', 'CommentId', 'DistrictId','POIName','TotalStar','Content','AuditTime','LastModifyTime','Score1','Score2','Score3','crawl_time']


xadmin.site.register(Target, TargetAdmin)
xadmin.site.register(SightInfo, SightInfoAdmin)
#xadmin.site.register(CommentInfo, CommentInfoAdmin)
xadmin.site.register(UserInfo, UserInfoAdmin)
xadmin.site.register(CommentInfo, CommentInfoAdmin)