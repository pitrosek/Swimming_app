"""
URL configuration for plavecke_zavody project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from zavody import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('zavody/', views.zavody_list, name='zavody_list'),
    path('zavody/<int:pk>/', views.zavod_detail, name='zavod_detail'),
    path('plavci/', views.plavci_list, name='plavci_list'),
    path('plavci/<int:pk>/', views.plavec_detail, name='plavec_detail'),
    path('kluby/', views.kluby_list, name='kluby_list'),
    path('kluby/<int:pk>/', views.klub_detail, name='klub_detail'),
    path('treneri/', views.treneri_list, name='treneri_list'),
    path('treneri/<int:pk>/', views.trener_detail, name='trener_detail'),
    path('treneri/add-sverenek/', views.add_sverenek, name='add_sverenek'),
    path('treneri/zapsat-plavce/', views.zapsat_plavce_na_zavod, name='zapsat_plavce_na_zavod'),
    path('treneri/pridat-plavce-do-klubu/', views.add_plavec_to_klub, name='add_plavec_to_klub'),
    path('stavy/', views.stat_list, name='stat_list'),
    path('stavy/<int:pk>/', views.stat_detail, name='stat_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
]
