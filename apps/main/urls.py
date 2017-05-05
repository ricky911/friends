from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
	url(r'^success$', views.friendsIndex),
	url(r'^profile/(?P<id>\d+)$', views.profile),
	url(r'^addFriend/(?P<id>\d+)$', views.addFriend),
	url(r'^delFriend/(?P<id>\d+)$', views.delFriend),
]