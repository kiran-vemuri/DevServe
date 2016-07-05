from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser, FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from django.core.urlresolvers import reverse
from django.conf import settings
from releases.serializers import ProductSerializer, ComponentSerializer, BinarySerializer
import os,  datetime, hashlib
from releases.models import Product, Component, Binary
from .forms import UploadFileForm

"""
generic function definitions
"""


def md5_cal(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()



"""
Handlers for UI actions follow!
"""


def product_index(request):
    """
    method to fetch list of available products and display them on the webpage
    :param request:
    :return:
    """
    product_list = Product.objects.order_by('name')
    context = {
        'product_list': product_list
    }
    return render(request, 'release_index.html', context)


def component_index(request, product_id):
    """
    method to fetch list of available components for the given product and display them on the web page
    :param request:
    :param product_id:
    :return:
    """
    component_list = Component.objects.filter(product_id=product_id)
    product_object = Product.objects.get(id=product_id)
    context = {
        'component_list': component_list,
        'product_object': product_object,
    }
    return render(request, 'component_index.html', context)


def binary_index(request, product_id, component_id):
    binary_list = Binary.objects.filter(component_id=component_id)
    component_object = Component.objects.get(id=component_id)
    product_object = Product.objects.get(id=product_id)
    context = {
        'binary_list': binary_list,
        'product_object': product_object,
        'component_object': component_object,
    }
    return render(request, 'binary_index.html', context)


def binary_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            component_obj = Component.objects.get(id=form.data['component'])
            binary_path = 'media/releases/'
            binary_path = os.path.join(binary_path, datetime.datetime.now().strftime('%Y_%m_%d'))
            if not os.path.exists(os.path.abspath(binary_path)):
                os.makedirs(binary_path)
            file_name = "%s_%s_%s_%s" %(component_obj.name,
                                     form.data['title'],
                                     str(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')),
                                        request.FILES['file'].name)
            binary_path = os.path.join(binary_path, file_name)
            binary_url = settings.DS_SERVER_IP+reverse('product_index')+binary_path
            if handle_uploaded_file(request.FILES['file'], binary_path):
                if form.data['notes']:
                    binary_object = Binary.objects.create(name=file_name,
                                                          component_id=form.data['component'],
                                                          path=binary_path,
                                                          url=binary_url,
                                                          notes=form.data['notes'],
                                                          md5sum=md5_cal(binary_path))
                    print binary_object.id
            return HttpResponseRedirect('/rest/binaries/'+str(binary_object.id))
    else:
        form = UploadFileForm()
    return render(request, 'binary_upload.html', {'form': form})


def handle_uploaded_file(in_file, binary_path):
    print binary_path
    """
    if not os.path.exists(os.path.abspath(binary_name)):
        try:
            os.makedirs(os.path.dirname(binary_name))
        except OSError as exc:
            raise
    """
    with open(binary_path, 'wb+') as destination:
        for chunk in in_file.chunks():
            destination.write(chunk)
        return True


def binary_status_change(request, product_id, component_id, binary_id, new_status):
    """
    Method to change the status on an uploaded binary.
    """
    binary_object = Binary.objects.get(id=binary_id)
    binary_object.status = new_status
    binary_object.save()
    redirect_url = "/releases/%s/%s/" % (str(product_id), str(component_id))
    return HttpResponseRedirect(redirect_url)




"""
Handlers for REST API follow!
"""


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited
    """
    queryset = Product.objects.all().order_by('create_date')
    serializer_class = ProductSerializer


class ComponentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows components to be viewed or edited
    """
    queryset = Component.objects.all().order_by('create_date')
    serializer_class = ComponentSerializer


class BinaryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows components to be viewed or edited
    """
    queryset = Binary.objects.all().order_by('upload_date')
    queryset = queryset.reverse()
    serializer_class = BinarySerializer
    parser_classes = (FormParser, MultiPartParser, )
    #parser_classes = (FileUploadParser,)

    def create(self, request):

        if request.data['name'] and request.data['notes'] and request.data['component_id'] and request.FILES['file']:
            component_id = request.data['component_id']
            component_obj = Component.objects.get(id=component_id)
            name = request.data['name']
            notes = request.data['notes']
            file_obj = request.FILES['file']

            file_name = "%s_%s_%s_%s" % (component_obj.name,
                                         name,
                                         str(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')),
                                         file_obj.name)

            binary_path = 'media/releases/'
            binary_path = os.path.join(binary_path, datetime.datetime.now().strftime('%Y_%m_%d'))
            if not os.path.exists(os.path.abspath(binary_path)):
                os.makedirs(binary_path)
            binary_path = os.path.join(binary_path, file_name)
            binary_url = "http://"+settings.DS_SERVER_IP + reverse('product_index') + binary_path



            print reverse('product_index')
            print settings.DS_SERVER_IP


            with open(binary_path, 'wb+') as destination:
                for chunk in file_obj.chunks():
                    destination.write(chunk)

            binary_object = Binary.objects.create(name=file_name,
                                                  component_id=component_id,
                                                  path=binary_path,
                                                  url=binary_url,
                                                  notes=notes,
                                                  md5sum=md5_cal(binary_path))

        return Response({'upload': 'success', 'binary_url': binary_url})

