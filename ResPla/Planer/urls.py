from django.conf.urls import patterns, url
from Planer import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^add_resource/$', views.AddResourceView.as_view(), name='add_resource'),
    )
