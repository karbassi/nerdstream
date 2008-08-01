from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

def index(request):
	users = models.Users.all().fetch(20)
	payload = dict(users=users)
	return render_to_response('index.html', payload)

def user(request, computer_name):
	user = models.Users.gql('WHERE computer_name = :1', computer_name).get()
	payload = dict(user=user)
	return render_to_response('user.html', payload)