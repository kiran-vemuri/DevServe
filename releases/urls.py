from django.conf.urls import url, patterns
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^$', views.product_index, name='product_index'),
    url(r'^fup$', views.file_upload),
    url(r'^sample$', views.sample_index),
    url(r'^(?P<product_id>[0-9]+)/$', views.component_index, name='component_index'),
    url(r'^(?P<product_id>[0-9]+)/(?P<component_id>[0-9]+)/$', views.binary_index, name='binary_index'),
    url(r'^binary_upload$', views.binary_upload, name='binary_upload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
