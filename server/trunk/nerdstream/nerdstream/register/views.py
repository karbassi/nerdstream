from django.http import HttpResponse, HttpResponseRedirect
from nerdstream.register import models
import nsforms
from django.shortcuts import render_to_response
	
def render(template, payload):
	# payload['recents'] = models.Users.all().fetch(5)
	return render_to_response(template, payload)

def index(request):
	users = models.Users.all().fetch(20)
	payload = dict(users=users)
	return render('index.html', payload)

def create_computer(request, computer_name):
	if request.method == 'GET':
		registerform = nsforms.RegisterForm()
	if request.method == 'POST':
		registerform = nsforms.RegisterForm(request.POST)
		if registerform.is_valid():
			user = registerform.save(commit=False)
			user.computer_name = computer_name
			user.save()
			registerform.save()
			return HttpResponseRedirect(user.get_absolute_url())
	payload = dict(registerform=registerform)
	return render('create.html', payload)

def user_config(request, computer_name):
	user = models.Users.gql('WHERE computer_name = :1', computer_name).get()
	payload = dict(user=user)
	return render_to_response('config.html', payload)