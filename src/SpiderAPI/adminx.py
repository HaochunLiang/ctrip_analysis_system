import xadmin
from xadmin import views

from .models import Target,SightInfo


class TargetAdmin(object):
  list_display = ['sid','did','cookie', 'add_time']
  search_fields = ['sid', 'did','cookie', 'add_time']
  list_filter = ['sid','did', 'cookie', 'add_time']

class SightInfoAdmin(object):
    list_display = ['Title', 'BusinessId', 'DistrictId','Tags','Texts','CommentScoreReal','CommentNumberText','AddressText','AddressWay','DescriptorText','Img']
    search_fields =['Title', 'BusinessId', 'DistrictId','Tags','Texts','CommentScoreReal','CommentNumberText','AddressText','AddressWay','DescriptorText','Img']
    list_filter =['Title', 'BusinessId', 'DistrictId','Tags','Texts','CommentScoreReal','CommentNumberText','AddressText','AddressWay','DescriptorText','Img']

class BaseSetting(object):
  enable_themes = True
  use_bootswatch = True


class GlobalSettings(object):
  site_title = u"携程旅游情感分析系统后台"
  site_footer = u"携程旅游情感分析系统"
  menu_style = "accordion"


xadmin.site.register(Target, TargetAdmin)
xadmin.site.register(SightInfo, SightInfoAdmin)
#xadmin.site.register(TweetsInfo, TweetsInfoAdmin)
#xadmin.site.register(CommentWeiboInfo, CommentWeiboInfoAdmin)
#xadmin.site.register(CommentInfo, CommentInfoAdmin)
#xadmin.site.register(ImgInfo, ImgInfoAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)