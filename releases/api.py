from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields
from releases.models import Binary, Component, Product


class ProductResource(ModelResource):
    class Meta:
        queryset = Product.objects.all()
        resource_name = 'product'
        excludes = ['path']


class ComponentResource(ModelResource):
    product = fields.ForeignKey(ProductResource, 'product')

    class Meta:
        queryset = Component.objects.all()
        resource_name = 'component'
        authorization = Authorization()


class BinaryResource(ModelResource):
    component = fields.ForeignKey(ComponentResource, 'component')
    # binary_file = fields.FileField(attribute="path")

    class Meta:
        queryset = Binary.objects.all()
        resource_name = 'binary'
        #authorization = Authorization()
