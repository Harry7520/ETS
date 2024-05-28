"""ETS_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from ETS_app.views import *

urlpatterns = [
    path('', local),
    path('m_main/', m_main),
    path('t_main/', t_main),
    path('c_login/', C_login, name="c_login"),
    path('c_register/', C_register, name="c_register"),
    path('c_logout/', C_logout),
    path('t_login/', T_login, name="t_login"),
    path('t_register/', T_register, name="t_register"),
    path('t_logout/', T_logout),
    path('m_login/', M_login, name="m_login"),
    path('m_register/', M_register, name="m_register"),
    path('m_logout/', M_logout),
    path('admin/', admin.site.urls),
    path('ets/', include('ETS_app.urls')),
    re_path(r'^.*/$', custom_404_view),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
