from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.product_index, name='product_index'),
    url(r'^fup$', views.file_upload),
    url(r'^sample$', views.sample_index),
    url(r'^(?P<product_id>[0-9]+)/$', views.component_index, name='component_index')
]
