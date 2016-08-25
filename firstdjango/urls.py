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

from django.conf.urls import url
from django.contrib import admin

#from inventory import views
from animeupload import views

urlpatterns = [
	url(r'^$',views.index, name='index'),
#	url(r'^item/(?P<id>\d+)/', views.item_detail, name='item_detail'),
    url(r'^show/(?P<id>\d+)/', views.show_detail, name='show_detail'),
    url(r'^admin/', admin.site.urls),
    url(r'^search/', views.search, name='search'),
    url(r'^rating_descriptions/', views.rating_descriptions, name='rating_descriptions'),
    url(r'^search_results/', views.search_results, name='search_results'),
#    url(r'^test/',views.test,name='test'),
    url(r'^ajax_test/',views.ajax_test,name='a_test'),
    url(r'^tag_search/',views.tag_search,name='tag_search'),
    url(r'^tag_results/',views.tag_results,name='tag_results'),
    url(r'^all_shows/',views.all_shows,name='all_shows'),
#    url(r'^simple_search/', view.ajax_test, name='test'),
#    url(r'^ajax/search/',views.ajax_search, name="ajax_search")
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#url(r'^(?P<show_name>)$')
