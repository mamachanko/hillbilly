from django.conf.urls.defaults import patterns, include, url

from hillbilly.guns.views import Guns


urlpatterns = patterns('',

    # traditional view
    url(r'^guns/$', 'guns.views.guns'),

    # class-based view
    url(r'^guns/$', Guns.as_view()),

    url(r'^guns/(?P<gun_id>\d+)/$', 'guns.views.get_gun_by_id'),
)
