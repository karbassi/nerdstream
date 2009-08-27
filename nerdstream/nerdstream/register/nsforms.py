from django import newforms as forms
import models
from google.appengine.ext.db import djangoforms

class RegisterForm(djangoforms.ModelForm):
	class Meta:
		model = models.Users
		exclude = ['interval', 'computer_name', 'start_time', 'end_time']