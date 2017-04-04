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

from django.core.exceptions import ValidationError



from django import forms
class ConsolidateForm(forms.Form):
	_selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
	title = forms.CharField(max_length=30)
	description = forms.CharField(max_length=150)

def consolidate(modelAdmin, request, queryset):#---disable consol of 1,split genre and tag
	from django.shortcuts import render
	from django.template.context_processors import csrf
	from django.http import HttpResponseRedirect
	args={}
#	print(modelAdmin)#--------------
#	temp = modelAdmin.makeanew("newgen","thing")
#	print(temp)
	args.update(csrf(request))
	form = None
	try:
		if 'apply' in request.POST:
#			print("apply in POST ......")#--------------
			form = ConsolidateForm(request.POST)

			if form.is_valid():
#				print("in form.is_valid() ......")#--------------
				title= form.cleaned_data['title']
				desc = form.cleaned_data['description']
				new_inst = modelAdmin.new_inst(title,desc)
				new_inst.clean_fields()

				if modelAdmin.is_dup(new_inst,queryset):
					raise ValidationError("not unique")

#				dup = Genre.objects.filter(name = new_genre.name).exclude(id__in =queryset)
#				if dup:
#					raise ValidationError("not unique")
				shows = modelAdmin.filter_shows(queryset)
				#vvvv shallow copy vvvvvv#
#				shows = Show.objects.filter(genres__in= queryset).distinct()

				new_inst.save()

				#update shows with new genre
				for show in shows:
					modelAdmin.set_to_show(new_inst,show)
#					print(show)
#					show.genres.add(new_genre)
#					show.save()

				#delete after update
				for curr in queryset:
					curr.delete()

				return HttpResponseRedirect(request.get_full_path())
		if not form:
			form = ConsolidateForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
	except ValidationError as e:
		args["message"] = "there was an integrity error"


	args["_selected_action"] = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
	args["queryset"] = queryset
	args["form"] = form
	return render_to_response('admin/consolidate.html',args)
consolidate.short_description = "Consolidate selected"

class AddTagForm(forms.Form):
	_selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
	tag = forms.ModelChoiceField(queryset=Tag.objects.all())

class AddGenreForm(forms.Form):
	_selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
	genre = forms.ModelChoiceField(queryset=Genre.objects.all())


def add_tag(self, request, queryset):
	from django.template.context_processors import csrf
	from django.http import HttpResponseRedirect
	args={}
	print(self)
	args["type"]= "tag"
	args["h_action"] = "add_tag"
	args.update(csrf(request))
	form = None

	if 'apply' in request.POST:
		form = AddTagForm(request.POST) #-----------here

		if form.is_valid():
			tag= form.cleaned_data['tag'] #-------------here
			for show in queryset:
				show.tags.add(tag) #--------------------here
			return HttpResponseRedirect(request.get_full_path())

	if not form:
		form = AddTagForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

	args["queryset"] = queryset
	args["form"] = form
	args["_selected_action"] = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
	return render_to_response('admin/add_tag.html',args)
add_tag.short_description = "Add tag to selected shows"

def add_genre(self, request, queryset):
	from django.template.context_processors import csrf
	from django.http import HttpResponseRedirect
	args={}
	args["type"]= "genre"
	args["h_action"] = "add_genre"
	args.update(csrf(request))
	form = None

	if 'apply' in request.POST:
		form = AddGenreForm(request.POST)

		if form.is_valid():
			genre= form.cleaned_data['genre'] #-------------here
			for show in queryset:
				show.genres.add(genre) #--------------------here
			return HttpResponseRedirect(request.get_full_path())

	if not form:
		form = AddGenreForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

	args["queryset"] = queryset
	args["form"] = form
	args["_selected_action"] = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
	return render_to_response('admin/add_tag.html',args)
add_genre.short_description = "Add genre to selected shows"

class showlistAdmin(admin.ModelAdmin):
	list_display = ['creator','title','likes']

class genreAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    actions=[consolidate]

    def new_inst(self,name,desc):
    	return Genre(name=name, description=desc)

    def is_dup(self,new_genre,queryset):
    	dup = Genre.objects.filter(name = new_genre.name).exclude(id__in =queryset)
    	if dup:
    		return True
    	return False

    def filter_shows(self,queryset):
    	return Show.objects.filter(genres__in= queryset).distinct()

    def set_to_show(self,genre,show):
    	show.genres.add(genre)
    	show.save()


class movieAdmin(admin.ModelAdmin):
	list_display = ['english_title']
	filter_horizontal = ['tags','genres',]
	actions=[add_tag,add_genre]

class tvshowAdmin(admin.ModelAdmin):
	list_display = ['english_title', 'total_episodes',]
	filter_horizontal = ['tags','genres',]
	actions=[add_tag,add_genre]

class tagAdmin(admin.ModelAdmin):
	list_display = ['name','description']
	actions=[consolidate]

	def new_inst(self,name,desc):
		return Tag(name=name, description=desc)

	def is_dup(self,new_tag,queryset):
		dup = Tag.objects.filter(name = new_tag.name).exclude(id__in =queryset)
		if dup:
			return True
		return False

	def filter_shows(self,queryset):
		return Show.objects.filter(tags__in= queryset).distinct()

	def set_to_show(self,tag,show):
		show.tags.add(tag)
		show.save()

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