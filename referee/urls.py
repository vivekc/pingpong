from django.conf.urls import url
from .views import JoinChampionship, IndexView
urlpatterns = [
    url(r'^start/$', IndexView.as_view(), name='start_referee'),
    url(r'^championship/join/(?P<player_id>[0-9]+)/$', JoinChampionship.as_view(), name="join_championship"),
    # url(r'^championship/join/$', JoinChampionship.as_view(), name="join_championship"),
]
