from django.conf.urls import patterns, url
from Planer import views

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^add_resource/$', views.AddResourceView.as_view(), name='add_resource'),
    url(r'^resource_list/$', views.ResourceListView.as_view(), name='resource_list'),
    )
