from django.db import models

LITE_TONE = NONE = 0
MODERATE_TONE = UNINTENTIONAL = CORPSE_LTE = LOW = ESRB_E = LIGHT = DAMN = UNDERWEAR = 1
DARK_TONE = MISCHIEVOUS = SILHOUETTE = MODERATE = ESRB_T = DEEP = CENCORED = 2
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

class Tag(models.Model):
	tag_name=models.CharField(max_length=30, unique=True)
	description = models.CharField(max_length=150,null=True)

	class Meta:
		ordering = ["tag_name"]

	def __str__(self):
		return self.tag_name

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

	image = models.FileField(default = "images/fnf/fnf.jpg", blank=True)
#	image = models.ImageField(upload_to="/images", default = images/fnf/fnf.jif, width_field = "width_field", height_field = "height_field")
#	height_field = models.IntegerField(default =0)
#	width_field = models.IntegerField(default =0)

#	tone = models.IntegerField(default = LITE_TONE, choices= tone_levels)
	english_title = models.CharField(max_length=200)
	japanese_title = models.CharField(max_length=200, null= True)
	description = models.TextField(max_length = 1000)
	total_episodes = models.IntegerField()
	ovas=  models.IntegerField(default = 0)
	movies = models.IntegerField(default = 0)
	total_seasons = models.IntegerField(default = 1)
	ongoing = models.BooleanField(default = False)

	series = models.ForeignKey(Series, null = True, blank = True, on_delete=models.SET_NULL)

	nudity = models.IntegerField(default = NONE, choices= n_choices)
	on_screen_intimacy = models.IntegerField(default = NONE, choices= osi_levels)
	sexual_intent = models.IntegerField(default = NONE, choices = si_levels)

	violence = models.IntegerField(default = NONE, choices= osv_levels)
	gore = models.IntegerField(default = NONE, choices= gore_levels)
	morbid_images = models.IntegerField(default = NONE, choices= mi_levels)

	feels = models.IntegerField(default = NONE, choices= emotional_challenge)
	profanity = models.IntegerField(default = NONE, choices= swares)
	moral_ambiguity = models.IntegerField(default = NONE, choices= ma_levels)

	tags = models.ManyToManyField(Tag, blank=True, null=True)

	def __str__(self):
		return self.english_title

	class Meta:
		ordering = ["english_title"]

#class Tag_relation(models.Model):
#	show = models.ForeignKey(Show, blank=True, null=True, on_delete=models.CASCADE)
#	tag = models.ForeignKey(Tag, blank=True, null=True, on_delete=models.CASCADE)

class Recommendation(models.Model):
	show = models.OneToOneField(Show, on_delete=models.CASCADE, null=True)
	recommended = models.CharField(max_length = 30)
	description = models.TextField(max_length = 300)