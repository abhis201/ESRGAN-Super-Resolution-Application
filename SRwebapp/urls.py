"""SRwebapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from . import views
from django.contrib.staticfiles.urls import  staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name = 'home'),
    path('loadimg',views.loadimg,name='loadimg'),
    path('makelr',views.makelr,name='makelr'),
    path('previmg',views.previmg,name='prev'),
    path('nextimg',views.nextimg,name='next'),
    path('SuperRes',views.applysr,name='applysr'),
    path('Results',views.nextpage,name='nextpage'),
    path('localclient',views.localclient,name='localclient'),
    path('showsr',views.clientrequest,name='showsr'),
    path('sendimages',views.transfer,name='transfer'),
    path('client',views.sendtoclient,name='client'),
    path('stop',views.stop,name="stop"),
    path('server',views.listenclient,name="listen")
]

urlpatterns += staticfiles_urlpatterns()