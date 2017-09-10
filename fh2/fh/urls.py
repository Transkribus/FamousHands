"""fh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'), #TODO BETTER REGEX FOR BOTH?
    url(r'^index$', views.index, name='index'),
    url(r'^search$', views.search, name='search'),
    url(r'^maps', views.maps, name='maps'),
    url(r'^login_process$', views.login_process, name='login_process'),
    url(r'^logout$', views.logout_process, name='logout_process'),
    url(r'^timeline$', views.timeline, name='timeline'),
    url(r'^upload_handwriting$', views.upload_handwriting, name='upload_handwriting'),
    url(r'^upload_handwriting_process$', views.upload_handwriting_process, name='upload_handwriting_process'),
    url(r'^upload_handwriting_process_imgs$', views.upload_handwriting_process_imgs, name='upload_handwriting_process_imgs'),
    url(r'^fh_admin$', views.admin, name='fh_admin'),
    url(r'^long_view$', views.long_view, name='long_view'),
    url(r'^longsearch$', views.longsearch, name='fh_longsearch'),
    url(r'^detail$', views.detail, name='detail'),
    url(r'^script$', views.script, name='script'), #just used for testing (TODO: better solution)
    url(r'^search_name_service', views.search_name_service, name='search_name_service'),
    url(r'^image_gallery', views.image_gallery, name='image_gallery'),
    url(r'^fh_admin', views.admin, name='fh_admin')
    
]
