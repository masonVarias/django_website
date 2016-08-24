import json from django.http
from django.http import Http404

def search(request):
	if request.is_ajax() and if request.method == "POST":

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

		emotion_max= request.POST["emotions_sel_high"]
		emotion_min= request.POST["emotions_sel_low"]
		profanity_max= request.POST["profanity_sel_high"]
		profanity_min= request.POST["profanity_sel_low"]

		shows = Show.objects.filter(
			nudity__lte = nudity_max, nudity__gte = nudity_min,
			on_screen_intimacy__lte = intimacy_max, on_screen_intimacy__gte = intimacy_min,
			sexual_intent__lte = intent_max, sexual_intent__gte = intent_min,
			violence__lte = violence_max, violence__gte = violence_min,
			gore__lte = gore_max, gore__gte = gore_min,
			feels__lte = emotion_max, feels__gte = emotion_min,
			profanity__lte = profanity_max, profanity__gte = profanity_min
			)

		html= render_to_string('test.html',{shows})
		res = {'html':html}
		return HttpResponce(json.dumps(res),"application/json")

	else:
		raise Http404


def test(request):
	if request.method =="POST":
		search_text = request.POST['search_text']
	else:
		search_text = ''

	results = Show.objects.filter(english_title__contains = search_text)


	args = {}
	args.update(csrf(request))

	args['results'] = results
	
	return render(request,'animeupload/ajax_test.html', args)