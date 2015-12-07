from django.conf.urls import patterns, url
from safewatch_ivr_app import views

urlpatterns = patterns('',
        url(r'^firstq/$', views.FirstQ, name = 'FirstQ'),
        url(r'^secondq/$', views.SecondQ, name = 'SecondQ'),
        url(r'^Thirdq/$', views.ThirdQ, name = 'ThirdQ'),
        url(r'^makecall/$', views.MakeCall, name = 'MakeCall'),
        url(r'^storedata/$', views.StoreData, name = 'StoreData')
)
