from django.contrib import admin
# Register your models here.
from .models import Show, Showlist, TVShow, Movie
from .models import Series
from .models import Tag
from .models import PrimaryLink, SecondaryLink
#from .models import Tag_relation
from .models import Recommendation
from .forms import SeriesForm
from .models import Genre

from django.shortcuts import render_to_response



from django import forms
class ConsolidateForm(forms.Form):
	_selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
	title = forms.CharField(max_length=30)
	description = forms.CharField(max_length=150)


def consolidate(modelAdmin, request, queryset):
	from django.shortcuts import render

	for item in queryset:
		print(item)
	args={}
	args["set"] = queryset
	return render(request, 'consolidate', args)

class AddTagForm(forms.Form):
	_selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
	tag = forms.ModelChoiceField(queryset=Tag.objects.all())

def add_tag(self, request, queryset):
	from django.template.context_processors import csrf
	from django.http import HttpResponseRedirect
	args={}
	args.update(csrf(request))
	form = None

	if 'apply' in request.POST:
		form = AddTagForm(request.POST)

		if form.is_valid():
			tag= form.cleaned_data['tag']
			for show in queryset:
				show.tags.add(tag)
			return HttpResponseRedirect(request.get_full_path())

	if not form:
		form = AddTagForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

	args["articles"] = queryset
	args["form"] = form
	args["_selected_action"] = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
	return render_to_response('admin/add_tag.html',args)
add_tag.short_description = "Add tag to selected shows"


class showlistAdmin(admin.ModelAdmin):
	list_display = ['creator','title','likes']

class genreAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    actions=[consolidate]

class movieAdmin(admin.ModelAdmin):
	list_display = ['english_title']
	filter_horizontal = ['tags','genres',]
	actions=[add_tag]

class tvshowAdmin(admin.ModelAdmin):
	list_display = ['english_title', 'total_episodes',]
	filter_horizontal = ['tags','genres',]
	actions=[add_tag]

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
admin.site.register(Movie, movieAdmin)
admin.site.register(TVShow, tvshowAdmin)
admin.site.register(Series,seriesAdmin)
admin.site.register(Tag, tagAdmin)
admin.site.register(Recommendation, recommendationAdmin)
admin.site.register(Showlist,showlistAdmin)
admin.site.register(PrimaryLink,linkAdmin)
admin.site.register(SecondaryLink,SecondaryLinkAdmin)