from django.conf.urls import patterns, url
from Planer import views

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^resource_add/$', views.AddResourceView.as_view(), name='resource_add'),
    url(r'^resource_list/$', views.ResourceListView.as_view(), name='resource_list'),
    url(r'^person_add/$', views.AddPersonView.as_view(), name='person_add'),
    url(r'^person_list/$', views.PersonListView.as_view(), name='person_list'),
    )
