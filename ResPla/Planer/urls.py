from django.conf.urls import patterns, url
from Planer import views

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(),
        name='index'),
    url(r'^resource_add/$', views.AddResourceView.as_view(),
        name='resource_add'),
    url(r'^resource_list/$', views.ResourceListView.as_view(),
        name='resource_list'),
    url(r'^person_add/$', views.AddPersonView.as_view(),
        name='person_add'),
    url(r'^person_list/$', views.PersonListView.as_view(),
        name='person_list'),
    url(r'^book_person/$', views.AddPersonBookingView.as_view(),
        name='book_person'),
    url(r'^book_resource/$', views.AddResourceBookingView.as_view(),
        name='book_respource'),
    url(r'^booking/list/all/$', views.BookingListAllView.as_view(),
        name='booking_list_all'),
    url(r'^booking/list/recent/$', views.BookingListRecentView.as_view(),
        name='booking_list_recent'),
    )
