from django.conf.urls import url
from . import views




urlpatterns = [
    url(r'^$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^reg_in_data$', views.reg_in_data),
    url(r'^log_in_data$', views.log_in_data),
    url(r'^clean_session$', views.clean_session),
    url(r'^trips/(?P<my_val>\d+)$', views.trips_info),
    url(r'^create_trip$', views.create_trip),
    url(r'^work_on_trip$', views.work_on_trip),
    url(r'^remove_trip/(?P<my_val>\d+)$', views.remove_trip),
    url(r'^edit_trip/(?P<my_val>\d+)$', views.edit_trip),
    url(r'^update_trip/(?P<my_val>\d+)$', views.update_trip)
]