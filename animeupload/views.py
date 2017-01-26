from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponseRedirect
from django.template.context_processors import csrf
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import get_object_or_404

from django.db.models import Q
from django.db import IntegrityError

from animeupload.forms import ShowListForm
from animeupload.models import Show,Showlist
#from animeupload.models import Tag_relation
from animeupload.models import Tag
from animeupload.models import Genre
from animeupload.models import Recommendation

from .models import PrimaryLink, SecondaryLink


def links(request):
	args={}
	#for sidebar
	args["shows"] = Show.objects.all()

	links_prim = PrimaryLink.objects.all()
	links_sec = SecondaryLink.objects.all()
	args["links"] = []

	args["plink"] = links_prim
	args["slink"] = links_sec

	if links_prim:
		for p_link in links_prim:
			args["links"].append(p_link)
			temp =[]
			if links_sec:
				for s_link in links_sec:
					if s_link.parent_link == p_link:
						args["links"].append(s_link)
					else:
						temp.append(s_link)
				links_sec = temp


	return render(request,"animeupload/links.html",args)

@login_required(login_url='/login/')
def get_profile(request):
	args = {}
	args['username'] = request.user.username
	args['showlists'] = Showlist.objects.filter(creator = request.user)
	return render(request,'registration/profile.html',args)

def removeshow(request):
	if request.method== "POST" and request.user.is_authenticated():
		shows = request.POST.getlist("remove")
		showlist_id = request.POST.get("showlist_id")
		if shows:
			curr_lists = Showlist.objects.filter(id = showlist_id)[0]
			for show_id in shows:
				curr_show = curr_lists.shows.get(id=show_id)
				curr_lists.shows.remove(curr_show);
			curr_lists.save();
			return HttpResponseRedirect('/accounts/profile')
	return HttpResponseRedirect('/')

def addtolist(request):
	args={}
	if request.method == 'POST' and request.user.is_authenticated():
		list_title = request.POST.get("lists")
		slist = Showlist.objects.get(title=list_title, creator = request.user)
		if slist:
			id_val = request.POST.get("added_show_id")
			show = Show.objects.get(id = id_val)
			slist.shows.add(show)
			#added show to list
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'),args)

def createlist(request):
	args={}
	if request.method =='POST' and request.user.is_authenticated():
		form = ShowListForm(request.POST)
		if form.is_valid():
			try:
				slist = form.save(commit = False)
				slist.creator = request.user
				slist.save()
				if request.POST.get("added_show_id"):
					id_val = request.POST.get("added_show_id")
					show = Show.objects.get(id=id_val)
					slist.shows.add(show)

			except IntegrityError as e:
				args['error'] = "already use that name"
				#better error message here -------------------
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'),args)

def deletelist(request):
#	args={}
	if request.method =='POST':
		passedid = request.POST.get("list_id")
		thelist = Showlist.objects.get(id=passedid)
		thelist.delete()

		return HttpResponseRedirect('/accounts/profile')
	return HttpResponseRedirect('/')

def login(request):
	args={}
	args.update(csrf(request))
	return render(request, login.html, args)

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/accounts/register/complete')
	else:
		form = UserCreationForm()
	token = {}
	token.update(csrf(request))
	token['form'] = form

	return render_to_response('registration/registration_form.html', token)

def registration_complete(request):
	return render_to_response('registration/registration_complete.html')

def index(request):
	shows = Show.objects.all()
	return render(request, 'animeupload/index.html', {
		'shows': shows,
		})
#	return HttpResponse('<p> in index view </p>')

def all_shows(request):
	shows = Show.objects.all()
	return render(request,'animeupload/all_shows.html',{
		'shows': shows,
		})

def show_detail(request, id):
	args = {}
	args['shows'] = Show.objects.all()
	if request.user.is_authenticated():
		args['showlists'] = Showlist.objects.filter(creator = request.user)
	tags= []
	try:
		show = Show.objects.get(id = id)
#		relations = Tag_relation.objects.filter(show = show)

#		for relation in relations:
#			tags.append(relation.tag)

		args['show'] = show
#		args['tags'] = tags

	except Show.DoesNotExist:
		raise Http404('no entry for this show')

	return render(request,'animeupload/show_detail.html', args)



def rating_descriptions(request):
	args = {}
	args['shows'] = Show.objects.all()
	return render(request,'animeupload/rating-descriptions.html',args)


def ajax_search(request):

	results = {}
	empty = True
	if request.method =="GET":
		search_text = request.GET['search_text'].strip()

		if search_text:
			results = Show.objects.filter(Q(english_title__contains = search_text) | Q(japanese_title__contains=search_text))
			empty = False

	else:
		search_text = ''

	args = {}
#	args.update(csrf(request))

	args['results'] = results
	args['empty'] = empty
	
	return render(request,'animeupload/ajax_test.html', args)

def search(request):
	args = {}
	args.update(csrf(request))
	args['tags'] = Tag.objects.all()
	args['genres'] = Genre.objects.all()
	args['choices'] = {"nudity": Show.n_choices,"intent":Show.si_levels, "intimacy": Show.osi_levels,
				"violence": Show.osv_levels, "gore":Show.gore_levels, "morbid": Show.mi_levels,
				"feels": Show.emotional_challenge, "profanity": Show.swares, "moral_a": Show.ma_levels,
				"fan_service": Show.fan_levels,}
	return render(request, 'animeupload/search.html', args)


def tag_filtering(shows,request):
	tags = request.POST.getlist('cb_tags')
	if tags:
		shows = Show.objects.filter(tags__in= tags).distinct()
	return shows

def genre_filtering(shows, request):
	genres = request.POST.getlist('cb_genres')
	if genres:
		shows = shows.filter(genres__in= genres).distinct()

	return shows;

def rating_filtering(shows, request):
#	try:
	nudity_max = request.POST.get("nudity_sel_high",100)
	nudity_min = request.POST.get("nudity_sel_low",0)
	intimacy_max = request.POST.get("intimacy_sel_high",100)
	intimacy_min = request.POST.get("intimacy_sel_low",0)
	intent_max = request.POST.get("intent_sel_high",100)
	intent_min = request.POST.get("intent_sel_low",0)

	violence_max = request.POST.get("violence_sel_high",100)
	violence_min = request.POST.get("violence_sel_low",0)
	gore_max = request.POST.get("gore_sel_high",100)
	gore_min = request.POST.get("gore_sel_low",0)
	morb_max = request.POST.get("morbid_images_sel_high",100)
	morb_min = request.POST.get("morbid_images_sel_low",0)

	emotion_max= request.POST.get("emotions_sel_high",100)
	emotion_min= request.POST.get("emotions_sel_low",0)
	profanity_max= request.POST.get("profanity_sel_high",100)
	profanity_min= request.POST.get("profanity_sel_low",0)
	moral_amb_max = request.POST.get("moral_ambiguity_sel_high",100)
	moral_amb_min = request.POST.get("moral_ambiguity_sel_low",0)

	fan_service_max = request.POST.get("fan_service_sel_high",100)
	fan_service_min = request.POST.get("fan_service_sel_low",0)

	shows = shows.filter(
	fan_service__lte = fan_service_max, fan_service__gte = fan_service_min,
	nudity__lte = nudity_max, nudity__gte = nudity_min,
	on_screen_intimacy__lte = intimacy_max, on_screen_intimacy__gte = intimacy_min,
	sexual_intent__lte = intent_max, sexual_intent__gte = intent_min,
	violence__lte = violence_max, violence__gte = violence_min,
	gore__lte = gore_max, gore__gte = gore_min,
	morbid_images__lte = morb_max, morbid_images__gte = morb_min,
	feels__lte = emotion_max, feels__gte = emotion_min,
	profanity__lte = profanity_max, profanity__gte = profanity_min,
	moral_ambiguity__lte = moral_amb_max, moral_ambiguity__gte = moral_amb_min,
	)
	

		
#	except MultiValueDictKeyError:
#		pass
	return shows

def recommendations(request):
	args = {}
	args["recommendations"] = Recommendation.objects.all()
	args["shows"] = Show.objects.all()
	return render(request,"animeupload/recommendations.html",args)

def search_results(request):
	args={}
	shows = Show.objects.all()
	shows = tag_filtering(shows,request)
	shows = genre_filtering(shows,request)
	shows = rating_filtering(shows,request)
	args["post"] = request.POST
	args["shows"] = shows
	return render(request, 'animeupload/search_results.html', args)

def tag_results(request):
	args = {}
	tags = request.POST.getlist('cb_tags')
#	shows = Tag_relation.objects.filter(tag_id__in = tags).values('show')
	shows = Show.objects.filter(tags__in= tags).distinct()
#	shows = Show.objects.filter(id__in = shows)
	args["shows"] = shows;
	return render(request, 'animeupload/search_results.html', args)
