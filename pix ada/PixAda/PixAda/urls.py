"""
URL configuration for PixAda project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include

##-------------------------  URLs  -------------------------##
'''
De Axius:
Cada que hagan una API nueva tienen que especificarla aquí para poder tener los links creados ahí con el siguiente formato:
    path('<nombreAPI>/', include('<nombreAPI>.urls'))

Pablo, ponte a estudiar HTML ctm
'''
urlpatterns = [
    path('admin/', admin.site.urls),
    path('FPixAda/', include('FPixAda.urls'))
]
