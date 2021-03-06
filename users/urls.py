from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from users import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^add$', views.add, name='add'),
    url(r'^resetFixture$', views.resetFixture, name='resetFixture'),
    url(r'^unitTests$', views.unitTests, name='unitTests')
    
)

urlpatterns += staticfiles_urlpatterns()

