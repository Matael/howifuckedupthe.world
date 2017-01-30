from django.conf.urls import url, include

from .views import index, EventDetail, event_vote, event_report, event_add

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^e/add/?', event_add, name="event#add"),
    url(r'^e/(?P<pk>\d+)/', include([
        url(r'^detail/?$', EventDetail.as_view(), name="event#detail"),
        url(r'^(?P<vote_order>(up)|(down))/?$', event_vote, name="event#vote"),
        url(r'^report/?$', event_report, name="event#report"),
    ]))
]
