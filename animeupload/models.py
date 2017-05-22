from django.db import models
from django.conf import settings

LITE_TONE = NONE = 0
SUBBED = MODERATE_TONE = UNINTENTIONAL = CORPSE_LTE = LOW = ESRB_E = LIGHT = DAMN = UNDERWEAR = 1
DUBBED = DARK_TONE = MISCHIEVOUS = SILHOUETTE = MODERATE = ESRB_T = DEEP = CENCORED = 2
ULTA_DARK_TONE = MALICE_LTE = DISMEMBERED = HIGH = ESRB_M = SEX = FUCK = BUTT = 3
MALICE_HVY = EXTREME = ESRB_A = BARBIE_SMOOTH = 4
OUTINES = 5
NIPPLE = 6
FULL_FRONTAL = 7


standard_choices = (
	(NONE,"none"),
	(LOW,"low"),
	(MODERATE,"moderate"),
	(HIGH,"high"),
	(EXTREME,"extreme"),
)

# Create your models here.
class Series(models.Model):
	series_name = models.CharField(max_length=200)
	watch_order = models.CharField(max_length=500)

	def __str__(self):
		return self.series_name
	class Meta:
		verbose_name_plural = "series"

class Tag(models.Model):
	name=models.CharField(max_length=30, unique=True)
	description = models.CharField(max_length=150,null=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.name = self.name.lower()
		super(Tag, self).save(*args, **kwargs)

class Genre(models.Model):
	name = models.CharField(max_length=30, unique=True)
	description = models.CharField(max_length=150,null=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
		return self.name

	def save(self,*args,**kwargs):
		self.name = self.name.lower()
		super(Genre, self).save(*args, **kwargs)

class Show(models.Model):

	n_choices= (
		(NONE,"none"),
		(UNDERWEAR,"underwear"),
		(CENCORED,"cencored"),
		(BUTT,"butt"),
		(BARBIE_SMOOTH,"barbie smooth"),
		(OUTINES,"outlined"),
		(NIPPLE,"nipple"),
		(FULL_FRONTAL,"full frontal"),
	)

	swares= (
		(NONE,"none"),
		(DAMN,"mild"),
		(CENCORED,"cencored"),
		(FUCK,"uncencored"),
	)
	osi_levels = (
		(NONE,"none"),
		(LIGHT,"light kissing"),
		(DEEP,"deep kissing/grope"),
		(SEX,"sex"),
	)

	osv_levels = (
		(NONE,"none"),
		(ESRB_E,"cartoon"),
		(ESRB_T,"blood"),
		(ESRB_M,"realistic"),
		(ESRB_A,"extreme"),
	)

	emotional_challenge = standard_choices

	mi_levels =(
		(NONE,"none"),
		(CORPSE_LTE,"unmarred dead"),
		(SILHOUETTE,"silhouetted dismemberment"),
		(DISMEMBERED,"dismemberment"),
	)
	gore_levels =standard_choices
		#none, lowblood, broken bone, cencored insideout, insideout

	fan_levels =standard_choices
	si_levels=(
		(NONE,"none"),
		(UNINTENTIONAL,"unintentional"),
		(MISCHIEVOUS,"mischievous"),
		(MALICE_LTE,"malicious(molestation)"),
		(MALICE_HVY,"extremley malicious(rape)"),
	)

	tone_levels=(
		(LITE_TONE,"light tone"),
		(MODERATE_TONE,"moderate tone"),
		(DARK_TONE,"dark tone"),
		(ULTA_DARK_TONE,"ultra dark tone"),
	)
	ma_levels = standard_choices

	image = models.FileField(default = "images/fnf/fnf.jpg", blank=True, upload_to='images/')

	english_title = models.CharField(max_length=200)
	japanese_title = models.CharField(max_length=200, null= True)
	description = models.TextField(max_length = 1000)

	length = models.IntegerField(null=True)

	series = models.ForeignKey(Series, null = True, blank = True, on_delete=models.SET_NULL)

#-------------------------------------------ratings-------------
	nudity = models.IntegerField(default = NONE, choices= n_choices)
	on_screen_intimacy = models.IntegerField(default = NONE, choices= osi_levels)
	sexual_intent = models.IntegerField(default = NONE, choices = si_levels)

	violence = models.IntegerField(default = NONE, choices= osv_levels)
	gore = models.IntegerField(default = NONE, choices= gore_levels)
	morbid_images = models.IntegerField(default = NONE, choices= mi_levels)

	feels = models.IntegerField(default = NONE, choices= emotional_challenge)
	profanity = models.IntegerField(default = NONE, choices= swares)
	moral_ambiguity = models.IntegerField(default = NONE, choices= ma_levels)

	fan_service = models.IntegerField(default = NONE, choices= fan_levels)
#---------------------------------------------------------------------------------
	tags = models.ManyToManyField(Tag, blank=True)
	genres = models.ManyToManyField(Genre, blank=True)

	modified_date = models.DateTimeField(auto_now=True, blank = True, null=True)
#---------------------------------------------------------------------------------
#	funimation = models.IntegerField(defalt = NONE, choices = audio_choices)
#	crunchyroll =

	def __str__(self):
		return self.english_title

	class Meta:
		ordering = ["english_title"]

	def save(self, *args, **kwargs):
		self.english_title = self.english_title.lower()
		self.japanese_title = self.japanese_title.lower()
		super(Show, self).save(*args, **kwargs)

class TVShow(Show):
	total_episodes = models.IntegerField()
	total_seasons = models.IntegerField(default = 1)
	ongoing = models.BooleanField(default = False)

class Movie(Show):
	def __str__(self):
		return self.english_title

class Recommendation(models.Model):
	show = models.OneToOneField(Show, on_delete=models.CASCADE, null=True)
	recommended = models.CharField(max_length = 30)
	description = models.TextField(max_length = 1000)
	tldr = models.TextField(max_length = 160, null = True, blank= True)

class Showlist(models.Model):
	creator = models.ForeignKey( settings.AUTH_USER_MODEL)
	title = models.CharField(max_length = 30)
	shows =  models.ManyToManyField(Show, blank=True)
	likes = models.IntegerField(default = 0)

	class Meta:
		unique_together = ('creator', 'title',)

class Link(models.Model):
	name = models.CharField(max_length = 30)
	description = models.TextField(max_length = 1000)
	home_page = models.URLField()
	#-------------------------------------------get/make color field
	color_f = models.CharField(max_length = 30, default="black")
	background = models.CharField(max_length = 30,default = "white")
#	color2 = models.CharField(max_length = 30)

#	image = models.FileField( blank=True, upload_to='images/')

	youtube = models.URLField(blank = True)
	twitter = models.URLField(blank = True)
	facebook = models.URLField(blank = True)
	instagram = models.URLField(blank = True)
	tumblr = models.URLField(blank = True)
	pintrest = models.URLField(blank = True)

	google_plus = models.URLField(blank = True)

	twitch = models.URLField(blank = True)
#	class Meta:
#		abstract = True

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.name = self.name.lower()
		super(Link, self).save(*args, **kwargs)


class PrimaryLink(Link):
	INDENT = "0px"
	def __str__(self):
		return self.name

class SecondaryLink(Link):
	INDENT = "50px"
	parent_link = models.ForeignKey(PrimaryLink, null=True, related_name="parent_lnk")

	def __str__(self):
		return self.name

class WatchOption(models.Model):
	audio_choices = (
		(SUBBED,"english subbed"),
		(DUBBED,"english dubbed"),
	)
	show = models.ForeignKey(Show, on_delete = models.CASCADE)
	link = models.ForeignKey(Link, on_delete = models.CASCADE)
	free = models.BooleanField(default = False)
	audio = models.IntegerField(default = None, choices=audio_choices)

	class Meta:
		unique_together = (("show","link"),)