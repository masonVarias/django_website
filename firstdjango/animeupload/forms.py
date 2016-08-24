# forms.py
from django import forms
from .models import Series
from .models import Tag
from .widgets import seriesWidget



class SeriesForm(forms.ModelForm):
	class Meta:
		model = Series
		fields = [ 'series_name', 'watch_order',]
#		exclude = ["watch_order"]
		widgets = {
			"watch_order" : seriesWidget(),
		}

#class tagSearchForm(forms.ModelForm):
#	class Meta:
#		model = Tag
#		fields = ['tag_name']
#		widgets = {
#			'tag_name' : CheckboxInput(),
#		}
