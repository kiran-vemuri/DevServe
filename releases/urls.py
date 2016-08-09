from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from releases import views


urlpatterns = [
    url(r'^$',
        views.product_index,
        name='product_index'),
    url(r'^(?P<product_id>[0-9]+)/$',
        views.component_index,
        name='component_index'),
    url(r'^(?P<product_id>[0-9]+)/(?P<component_id>[0-9]+)/$',
        views.binary_index,
        name='binary_index'),
    url(r'^binary_status/(?P<product_id>[0-9]+)/(?P<component_id>[0-9]+)/(?P<binary_id>[0-9]+)/(?P<new_status>[a-z]+)/$',
        views.binary_status_change,
        name='binary_status'),
    url(r'^binary_upload$',
        views.binary_upload,
        name='binary_upload'),
    url(r'^activity_report/$', views.activity_report)
    # url(r'^admin_action/clear_unstable_binaries', views.clear_unstable_binaries),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
