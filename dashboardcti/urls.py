"""dashboardcti URL Configuration

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

from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('maingui.urls')),
    path('users/', include('users.urls')),
    path('profiles/', include('profiles.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('agent_console/', include('agent_console.urls')),
    path('form_creator/', include('form_creator.urls')),
    path('motivos/', include('motivos.urls')),
    path('sedes/', include('sedes.urls')),
    path('asesores/', include('asesores.urls')),
    path('consolidacion/', include('consolidacion.urls')),
    path('campaigns/', include('campaigns.urls')),
]

urlpatterns += staticfiles_urlpatterns()
