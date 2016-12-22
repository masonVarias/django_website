"""firstdjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
#from inventory import views
from animeupload import views

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

urlpatterns = [
	url(r'^$',views.index, name='index'),
    url(r'^show/(?P<id>\d+)/', views.show_detail, name='show_detail'),
    url(r'^admin/', admin.site.urls),
    url(r'^search/', views.search, name='search'),
    url(r'^rating_descriptions/', views.rating_descriptions, name='rating_descriptions'),
    url(r'^search_results/', views.search_results, name='search_results'),
#    url(r'^test/',views.test,name='test'),
    url(r'^ajax_search/',views.ajax_search,name='a_search'),
#    url(r'^tag_search/',views.tag_search,name='tag_search'),
#    url(r'^tag_results/',views.tag_results,name='tag_results'),
    url(r'^all_shows/',views.all_shows,name='all_shows'),
    url(r'^recommendations/',views.recommendations,name='recommendations'),
    url(r'^login/', auth_views.login, name="my_login"),
    url(r'^accounts/profile/',views.get_profile, name="my_profile"),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/createList/',views.createlist, name="create_list"),
    url(r'^accounts/deleteList/',views.deletelist, name="delete_list"),
    url(r'^accounts/removeShow/',views.removeshow, name="remove_show"),
   # url(r'^logout/',auth_views.logout,name="my_logout"),
   # url(r'^accounts/register/$', views.register, name='my_register'),
   # url(r'^accounts/register/complete/$', views.registration_complete, name='my_registration_complete'),
#    url(r'^ajax/search/',views.ajax_search, name="ajax_search")
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#url(r'^(?P<show_name>)$')
