from django import template
from django.utils.html import format_html
from django.utils.html import escape
from django.utils.html import mark_safe
from animeupload.models import Show
#from models import Show
#----------------check here for xss
register = template.Library()

@register.simple_tag
def display_rating(passed_value, choices=[]):
#		string = format_html("<h3>{0}: {1}</h3>",escape(passed_title),passed_value)
#		string = string + format_html('<meter id = "meter_item" min = "0" optimum = "{2}" low = "{3}" max = "{1}" value ="{0}"></meter>', escape(passed_value),choices[-1][-1],)
		string = create_meter(	passed_value,get_max(choices)	)

		string = string+ format_html('<ul id="scale">')
		for key,value in choices:
			if(key == passed_value):
				value = format_html("<b>{}</b>",value)

			string = string + format_html('<li><span id="scale">{}</span></li>',value)

		string = string + format_html("</ul>")
		return string

@register.simple_tag
def get_all_shows_alp():
	shows = Show.objects.all()
	string = format_html("")
	alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
	string = format_html('<div class="col-sm-6">')

	for letter in alphabet:
		if letter == "N":
			string = string + format_html('</div><div class="col-sm-6">')

		string = string + create_letter(letter)
		string = string + list_shows_by_letter(shows.filter(english_title__startswith=letter))

	string = string + format_html("</div>")
	return string

def list_shows_by_letter(shows):
	string = format_html("<ul>")
	for show in shows:
		string = string + format_html('<li><a href = "/show/{0}">{1}</a></li>',show.id,show.english_title.capitalize())

	string = string + format_html("</ul>")
	return string

def create_letter(letter):
	return format_html('<h2 class="{0}">{0}</h2>',letter)

def create_meter(val, total):
	opt = int(total)/2
	meter = format_html('<meter id = "meter_item" low = "{3}" optimum="{2}" max = "{1}" value ="{0}"></meter>', val, total, opt, opt + 1)
#	meter = meter + format_html("<h1>{1}:{0}</h1>",total,val)
	return meter

@register.simple_tag
def get_max(choices=[]):
	return escape(choices[-1][0])

@register.simple_tag
def create_search_slider_html(name, choices=[]):
	name = escape(name)
	html = create_header(name)
	html = html + create_search_dropdown(name,False,choices)
	html = html + create_search_dropdown(name,True,choices)
	return html

def create_header(name):
	if "_" in name:
		name = name.replace('_',' ')

	html = format_html("<h4>{0}</h4>",name) #---------------------------------should be divs
	return html

def create_search_dropdown(name,is_max,choices):
	if " " in name:
		name = name.replace(' ','_')
		
	html = create_label(name,is_max)
	html = html + open_select(name,is_max)
	html = html + create_options(choices, is_max)
	html = html + close_select()
	return html


def create_label(name,is_max):
	limit = high_or_low(is_max)

	string =  format_html('<label for="{0}_sel_{1}">{1}</label>',name,limit)
	return string

def open_select(name,is_max):
	limit = high_or_low(is_max)

	string = format_html('<select name="{0}_sel_{1}" id ="{0}_sel_{1}">',name,limit)
	return string

def close_select():
	return format_html('</select>')


def create_options(choices,is_max):
	string = format_html("")
	selected = ""
	total = len(choices) -1
	i = 0

	for val,name in choices:
		if i == total and is_max:
			selected = "selected"

		string = string + format_html('<option value="{0}" {2}>{1}</option>',escape(val),escape(name),selected)
		i = i +1

	return string

def high_or_low(is_max):
	if is_max:
		return "high"
	return "low"


@register.simple_tag
def series_selector_img_li(show):
	html = format_html("")
#put in try catch
#	try:
	html = create_img_tag(show.image, "img-rounded")
#	html = html + format_html("<h5>{}</h5>",show.english_title)
	html = create_li_tag(html)

	return html



def create_img_tag(img,img_class ="",img_id =""):
	return format_html("<img src = '{0}' height = '100px' width = '80px' id ='{1}' class = '{2}'>",img, img_id, img_class)


def create_li_tag(content, li_class="", li_id=""):
	return format_html("<li id='{1}' class = '{2}'>{0}</li>",content,escape(li_id),escape(li_class))



#code found at https://djangosnippets.org/snippets/1357/
@register.filter
def get_range( value ):
  """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
  """
  return range( value )

@register.simple_tag
def display_series (series, curr_id):
#	if series not set
	season = format_html("")
	if series == None:
		return format_html("<b>not available</b>")

	html =format_html("")
	arr = series.watch_order.split(',')

	arrow = format_html("""<div class='col-sm-2'>
											<svg width="100%">
												  	<line x1="0" y1="50%" x2="100%" y2="50%" style="stroke:rgb(255,0,0);stroke-width:2" />

													<line x1="80%" y1="40%" x2="100%" y2="50%" style="stroke:rgb(255,0,0);stroke-width:2" />

													<line x1="80%" y1="60%" x2="100%" y2="50%" style="stroke:rgb(255,0,0);stroke-width:2" /> 
											</svg>
										</div>""")

	series = iter(arr)
	show = next(series)
	html = format_series(show,curr_id)

	for show in series:
#		if ':' in show:
#			show = show.split(':')
#			season = " season " + show[1]
#			show = show[0]

#		curr = Show.objects.get(id=show)
#		if show != arr[0]:
			html = html + arrow
			html = html + format_series(show,curr_id)
#		title = curr.english_title
#		content = format_html("{0}{1}", title, season)

#		if int(show) != int(curr_id):
#			content = format_html("<a href ='/show/{0}''>{1}</a>",curr.id,content)
#		html = html + format_html("<div class='col-sm-2' style='text-align:center; outline:1px solid black;'>{0}</div>",content)
	return mark_safe(html + "<br>")


def format_series(show, curr_id):
	season = format_html("")
	#if split by season
	if ':' in show:
		show = show.split(':')
		season = " season " + show[1]
		show = show[0]

	curr = Show.objects.get(id=show)
	content = format_html("{0}{1}", curr.english_title, season)

	#remove link to self
	if int(show) != int(curr_id):
		content = format_html("<a href ='/show/{0}''>{1}</a>",curr.id,content)
	html = format_html("<div class='col-sm-2' style='text-align:center; outline:1px solid black;'>{0}</div>",content)
	return html

