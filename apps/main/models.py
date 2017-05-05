# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re, bcrypt

class UserManager(models.Manager):
	def validateUser(self, post):
		is_valid = True
		errors = []
		if len(post.get('name')) < 2 or len(post.get('name')) == 0:
			is_valid = False
			errors.append('Name must be at least 2 characters')
		if len(post.get('alias')) < 2 or len(post.get('alias')) == 0:
			is_valid = False
			errors.append('Alias must be at least 2 characters')
		if not re.search(r'\w+\@\w+\.\w+', post.get('email')):
			is_valid = False
			errors.append('Please enter a valid email')
		if len(post.get('password')) < 8:
			is_valid = False
			errors.append('Password must be at least 8 characters')
		if post.get('password') != post.get('confirm_password'):
			is_valid = False
			errors.append('Passwords do not match')
		return {'status': is_valid, 'errors': errors}

	def registerUser(self, post):
		return User.objects.create(
			name = post.get('name'),
			alias = post.get('alias'),
			email = post.get('email'),
			password = bcrypt.hashpw(post.get('password').encode(), bcrypt.gensalt()),
			) 

	def loginUser(self, post):
		user = User.objects.filter(email = post.get('email')).first()
		if user and bcrypt.hashpw(post.get('password').encode(), user.password.encode()) == user.password:
			return {'status': True, 'user': user}
		else:
			return {'status': False}

class User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	friend = models.ManyToManyField('self', related_name='friends')
	confirm_password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()
# Create your models here.
