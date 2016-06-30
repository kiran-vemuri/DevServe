from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
import json, os
from .models import Product, Component, Binary
from .forms import UploadFileForm


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
    context = {
        'binary_list': binary_list,
        'product_id': product_id,
        'component_object': component_object,
    }
    return render(request, 'binary_index.html', context)


def binary_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            component_object = Component.objects.get(id=form.data['component'])
            product_object = Product.objects.get(id=component_object.product_id)
            binary_path = product_object.path + component_object.path
            binary_object = Binary.objects.create(name='test', component_id=form.data['component'], path=binary_path)
            handle_uploaded_file(request.FILES['file'], binary_path)
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'binary_upload.html', {'form': form})


def handle_uploaded_file(in_file, binary_path):
    print binary_path
    if not os.path.exists(os.path.abspath(binary_path)):
        try:
            os.makedirs(os.path.dirname(binary_path))
        except OSError as exc:
            raise
    with open('media/name.txt', 'wb+') as destination:
        for chunk in in_file.chunks():
            destination.write(chunk)


def sample_index(request):
    context = {'page_title': 'Test'}
    return render(request, 'base.html', context)


def file_upload(request):
    if request.method == 'POST':
        if request.FILES:
            with open('/tmp/devservetestfile', 'wb+') as destination:
                for chunk in request.FILES['file']:
                    destination.write(chunk)
    return render(request, (json.dumps({'result': 'success'})))
