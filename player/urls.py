from django.conf.urls import url

from player.views import PlayerDashboard

urlpatterns = [
    url(r'^dashboard/$', PlayerDashboard.as_view(), name='start_referee'),
]