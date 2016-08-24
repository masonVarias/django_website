from django.shortcuts import render
from django.http import Http404
from django.template.context_processors import csrf


from animeupload.models import Show
#from animeupload.models import Tag_relation
from animeupload.models import Tag

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

	return render(request,'animeupload/show_detail.html', args
		)

def search(request):
	choices = {"nudity": Show.n_choices,"intent":Show.si_levels, "intimacy": Show.osi_levels,
				"violence": Show.osv_levels, "gore":Show.gore_levels, "morbid": Show.mi_levels,
				"feels": Show.emotional_challenge, "profanity": Show.swares, "moral_a": Show.ma_levels,}
	return render(request, 'animeupload/search.html', {
		'choices': choices,
		})

def rating_descriptions(request):
	return render(request,'animeupload/rating-descriptions.html')

def search_results(request):
	try:
#		print(request.POST)
#	if request.method == "POST":
		nudity_max = request.POST["nudity_sel_high"]
		nudity_min = request.POST["nudity_sel_low"]
		intimacy_max = request.POST["intimacy_sel_high"]
		intimacy_min = request.POST["intimacy_sel_low"]
		intent_max = request.POST["intent_sel_high"]
		intent_min = request.POST["intent_sel_low"]

		violence_max = request.POST["violence_sel_high"]
		violence_min = request.POST["violence_sel_low"]
		gore_max = request.POST["gore_sel_high"]
		gore_min = request.POST["gore_sel_low"]
		morb_max = request.POST["morbid_images_sel_high"]
		morb_min = request.POST["morbid_images_sel_low"]

		emotion_max= request.POST["emotions_sel_high"]
		emotion_min= request.POST["emotions_sel_low"]
		profanity_max= request.POST["profanity_sel_high"]
		profanity_min= request.POST["profanity_sel_low"]
		moral_amb_max = request.POST["moral_ambiguity_sel_high"]
		moral_amb_min = request.POST["moral_ambiguity_sel_low"]

		shows = Show.objects.filter(
			nudity__lte = nudity_max, nudity__gte = nudity_min,
			on_screen_intimacy__lte = intimacy_max, on_screen_intimacy__gte = intimacy_min,
			sexual_intent__lte = intent_max, sexual_intent__gte = intent_min,
			violence__lte = violence_max, violence__gte = violence_min,
			gore__lte = gore_max, gore__gte = gore_min,
			morbid_images__lte = morb_max, morbid_images__gte = morb_min,
			feels__lte = emotion_max, feels__gte = emotion_min,
			profanity__lte = profanity_max, profanity__gte = profanity_min,
			moral_ambiguity__lte = moral_amb_max, moral_ambiguity__gte = moral_amb_min
			)

		return render(request, 'animeupload/search_results.html', {
		'shows': shows,
		})

	except Show.DoesNotExist:
		raise Http404('no entry for this show')

def tag_search(request):
	args = {}
	args.update(csrf(request))

	args['tags'] = Tag.objects.all()
	
	return render(request,'animeupload/tag_search.html',args
		)

def tag_results(request):
	tags = request.POST.getlist('cb_tags')
#	shows = Tag_relation.objects.filter(tag_id__in = tags).values('show')
	shows = Show.objects.filter(tags__in= tags).distinct()
#	shows = Show.objects.filter(id__in = shows)

	return render(request, 'animeupload/search_results.html', {
		 'shows' : shows,
		})

def ajax_test(request):

	results = {}
	empty = True
	if request.method =="GET":
		search_text = request.GET['search_text'].strip()

		if search_text:
			results = Show.objects.filter(english_title__contains = search_text)
			empty = False

	else:
		search_text = ''

	args = {}
#	args.update(csrf(request))

	args['results'] = results
	args['empty'] = empty
	
	return render(request,'animeupload/ajax_test.html', args)