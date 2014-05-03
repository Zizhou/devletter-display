from django.conf.urls import patterns, url

from display import views

urlpatterns = patterns('',
    url(r'^$', views.main_page, name = 'main'),
    url(r'^devlist/', views.devlist, name = 'devlist'),
    url(r'^gamelist/', views.gamelist, name = 'gamelist'),
    url(r'^profile/(?P<dev_id>\d+)/$', views.profile, name = 'profile'),
)
