from django.shortcuts import render, get_list_or_404
import json
from .models import Product, Component, Binary


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
    component_list = get_list_or_404(Component, product_id=product_id)
    context = {
        'component_list': component_list,
    }
    return render(request, 'component_index.html', context)


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
