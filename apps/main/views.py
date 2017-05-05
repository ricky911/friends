# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
	return render(request, 'main/index.html')

def currentUser(request):
	if 'user_id' in request.session:
		return User.objects.get(id=request.session['user_id'])

def register(request):
	if request.method != 'POST':
		return redirect('/')
	else:
		check = User.objects.validateUser(request.POST)
		# print check['status']
		if check['status'] == True:
			user = User.objects.registerUser(request.POST)
			request.session['user_id'] = user.id
			return redirect('/success')
		else:
			for error in check['errors']:
				messages.add_message(request, messages.ERROR, error, extra_tags='register')
				return redirect('/')

def login(request):
	if request.method != 'POST':
		return redirect('/')
	else:
		check = User.objects.loginUser(request.POST)
		# print check['status']
		if check['status'] == True:
			request.session['user_id'] = check['user'].id
			return redirect('/success')
		else:
			messages.add_message(request, messages.ERROR, 'Invalid credentials', extra_tags='login')
			return redirect('/')

def friendsIndex(request):
	friends = []
	for user in User.objects.all().exclude(friend=currentUser(request)):
		if user != currentUser(request):
			friends.append(user)
	context = {
		'user': currentUser(request),
		'friends': friends,
	}
	return render(request, 'main/friends.html', context)

def profile(request, id):
	user = User.objects.get(id=id)
	context = {
		'user': user,
	}
	return render(request, 'main/profile.html', context)

def addFriend(request, id):
	friends = User.objects.get(id=id)
	currentUser(request).friend.add(friends)
	return redirect('/success')

def delFriend(request, id):
	friends = User.objects.get(id=id)
	currentUser(request).friend.remove(friends)
	return redirect('/success')


def logout(request):
	request.session.clear()
	return redirect('/')

# Create your views here.
