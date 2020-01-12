"""ctrip_analysis_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView,RedirectView
from SpiderAPI.views import SpiderCtrip
from SnowNLPAPI.views import SnowNLPCtrip

import xadmin

urlpatterns = [
    #path('admin/', admin.site.urls),
    path(r'^$', TemplateView.as_view(template_name="index.html")),
    path('xadmin/', xadmin.site.urls),
    path('spiderapi/', SpiderCtrip.SpiderAPI, name="spiderapi"),
    path('wordcloudapi/', SpiderCtrip.WordCloudAPI, name="wordcloudapi"),
    path('commentsapi/', SpiderCtrip.CommentsAPI, name="commentsapi"),

    path('snownlpapi/', SnowNLPCtrip.SnowNLPAPI, name="snownlpapi"),
    path('favicon.ico', RedirectView.as_view(url='static/favicon.ico')),

]
