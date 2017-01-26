from django.contrib import admin
# Register your models here.
from .models import Show, Showlist
from .models import Series
from .models import Tag
from .models import PrimaryLink, SecondaryLink
#from .models import Tag_relation
from .models import Recommendation
from .forms import SeriesForm
from .models import Genre


class showlistAdmin(admin.ModelAdmin):
	list_display = ['creator','title','likes']

class genreAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


class showAdmin(admin.ModelAdmin):
	list_display = ['english_title', 'total_episodes']
	filter_horizontal = ['tags','genres',]


class tagAdmin(admin.ModelAdmin):
	list_display = ['tag_name','description']

class seriesAdmin(admin.ModelAdmin):
	list_display = ['series_name']
	form = SeriesForm

class recommendationAdmin(admin.ModelAdmin):
	list_display = ['show','recommended']

class linkAdmin(admin.ModelAdmin):
	list_display = ['name','home_page']

class SecondaryLinkAdmin(admin.ModelAdmin):
	list_display = ['name','parent_link']

admin.site.register(Genre, genreAdmin)
admin.site.register(Show, showAdmin)
admin.site.register(Series,seriesAdmin)
admin.site.register(Tag, tagAdmin)
admin.site.register(Recommendation, recommendationAdmin)
admin.site.register(Showlist,showlistAdmin)
admin.site.register(PrimaryLink,linkAdmin)
admin.site.register(SecondaryLink,SecondaryLinkAdmin)