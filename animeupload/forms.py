# forms.py
from django import forms
from .models import Series
from .models import Tag
from .models import Showlist
from .widgets import seriesWidget
from django.contrib.auth.models import User



class SeriesForm(forms.ModelForm):
	class Meta:
		model = Series
		fields = [ 'series_name', 'watch_order',]
#		exclude = ["watch_order"]
		widgets = {
			"watch_order" : seriesWidget(),
		}

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ['username', 'email', 'password']

class ShowListForm(forms.ModelForm):
	class Meta:
		model = Showlist
		fields = ('title',)