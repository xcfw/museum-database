from django.conf.urls import url
from . import views

app_name = 'museum'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^collections/$', views.collections, name='collections'),
	url(r'^items/$', views.items, name='items'),
	url(r'^collections/(?P<ref>[%&+ \w]+)/$', views.collectionView, name='collection'),
	url(r'^items/(?P<ref>[%&+ \w]+)/$', views.itemView, name='item'),
]

