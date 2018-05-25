from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^add$',views.add),
    url(r'^create$',views.create_trip),
    url(r'^logout$',views.logout),
    url(r'^destination/(?P<number>\d+)$',views.show),
    url(r'^join/(?P<number>\d+)$',views.join)

]
