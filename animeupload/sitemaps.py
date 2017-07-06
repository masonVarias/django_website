from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from animeupload.models import Tag, Show, Genre,Recommendation
import datetime

class StaticViewSitemap(Sitemap):
	changefreq = "monthly"
	priority = 1.0
	lastmod = datetime.datetime.now()

	def items(self):
		return ['index','rating_descriptions','search','all_shows','recommendations','my_login','my_profile','links','all_tags','all_genres']

	def location(self, item):
		return reverse(item)

class TagSitemap(Sitemap):
	changefreq = "monthly"
	priority = 1.0
	lastmod = datetime.datetime.now()

	def items(self):
		return Tag.objects.all()

class GenreSitemap(Sitemap):
	changefreq = "monthly"
	priority = 1.0
	lastmod = datetime.datetime.now()

	def items(self):
		return Genre.objects.all()

class ShowSitemap(Sitemap):
	changefreq = "monthly"
	priority = 1.0
	lastmod = datetime.datetime.now()

	def items(self):
		return Show.objects.all()