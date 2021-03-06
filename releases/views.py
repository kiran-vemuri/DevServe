from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser, FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
import logging
from logging.config import dictConfig


from releases.serializers import ProductSerializer, ComponentSerializer, BinarySerializer
import os,  datetime, hashlib
from releases.models import Product, Component, Binary, EventLog
from .forms import UploadFileForm

"""
logger
"""
# TODO:
# logfile = os.path.abspath("/media/logs/devserve.log")
#
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# handler = logging.FileHandler(logfile)
# handler.setLevel(logging.INFO)
#
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
#
# logger.addHandler(handler)

"""
generic function definitions
"""


def md5_cal(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# TODO:
def remove_file(fpath):
    #fpath = "/Users/kvemuri/Documents/KiranRepos/DevServe/media/releases/2016_07_15/SQA_ReleaseManagement_releaseupload_2016_07_15_12_16_33_devserve_upload.py_bak"
    print fpath
    print os.path.dirname(fpath)
    if os.path.exists(fpath) and os.path.isfile(fpath):
        os.remove(fpath)
    print os.listdir(os.path.dirname(fpath))
    logger.info(os.listdir(os.path.dirname(fpath)))


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
    return render(request, 'releases/release_index.html', context)


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
    return render(request, 'releases/component_index.html', context)


def binary_index(request, product_id, component_id):
    binary_list = Binary.objects.filter(component_id=component_id).order_by('-upload_date')
    component_object = Component.objects.get(id=component_id)
    product_object = Product.objects.get(id=product_id)
    context = {
        'binary_list': binary_list,
        'product_object': product_object,
        'component_object': component_object,
    }
    return render(request, 'releases/binary_index.html', context)


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
            binary_url = "http://"+settings.DS_SERVER_IP+reverse('product_index')+binary_path
            if handle_uploaded_file(request.FILES['file'], binary_path):
                if form.data['notes']:
                    binary_object = Binary.objects.create(name=file_name,
                                                          component_id=form.data['component'],
                                                          path=binary_path,
                                                          url=binary_url,
                                                          notes=form.data['notes'],
                                                          md5sum=md5_cal(binary_path))
                    print binary_object.id
                    event_log = "Developer_Notes: {}".format(binary_object.notes)
                    event_object = EventLog.objects.create(binary=binary_object,
                                                           component_name=component_obj.name,
                                                           status_change="upload",
                                                           event_log=event_log)
                    print "New event: {}".format(event_object.event_log)
            return HttpResponseRedirect('/rest/binaries/'+str(binary_object.id))
    else:
        form = UploadFileForm()
    return render(request, 'releases/binary_upload.html', {'form': form})


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
    component_obj = Component.objects.get(id=binary_object.component.id)
    binary_object.status = new_status
    # binary_object.save()
    redirect_url = "/releases/%s/%s/" % (str(product_id), str(component_id))
    if request.method == 'POST':
        binary_object.change_notes = request.POST.get("change_notes")
        binary_object.bug_url = request.POST.get("bug_url")
        binary_object.save()
        if binary_object.bug_url == "":
            event_log = "Change_Notes: '{}' ".format(binary_object.change_notes)
        else:
            event_log = "Change_Notes: '{}' and Bug: '{}'".format(binary_object.change_notes,
                                                                  binary_object.bug_url)
        event_object = EventLog.objects.create(binary=binary_object,
                                               component_name=component_obj.name,
                                               status_change=binary_object.status,
                                               event_log=event_log)
        print "New event: {}".format(event_object.event_log)
    else:
        binary_object.status = new_status
        binary_object.save()
        event_object = EventLog.objects.create(binary=binary_object,
                                               component_name=component_obj.name,
                                               status_change=binary_object.status,
                                               event_log='')
        print "New event: stable/production"
    return HttpResponseRedirect(redirect_url)


def activity_report(request):
    binary_list = Binary.objects.all().order_by('-status_change_date')
    component_list = Component.objects.all()
    event_list = EventLog.objects.all().order_by('-event_date')
    event_date_list = EventLog.objects.datetimes('event_date', 'day', order="DESC")
    upload_count_list = []
    for component in component_list:
        upload_count_list.append((component.name, len(Binary.objects.filter(component=component))))
    modify_count_list = []
    for component in component_list:
        modify_count_list.append((component.name, len(Binary.objects.filter(component=component))))
    context = {
        'event_list': event_list,
        'event_date_list': event_date_list,
        'component_list': component_list,
        'upload_count_list': upload_count_list,
        'modify_count_list': modify_count_list
    }
    # print EventLog.objects.datetimes('event_date', 'day', order="DESC")
    # print "month"
    # print EventLog.objects.datetimes('event_date', 'month', order="DESC")
    # print EventLog.objects.filter(event_date__date=datetime.date(2016, 8, 10))
    # print "mnth---->"
    # mnth_list = EventLog.objects.filter(event_date__month=8)
    # print mnth_list.filter(event_date__date=datetime.date(2016, 8, 10))
    return render(request, 'releases/activity_report.html', context)


def activity_report_month(request, a_year, a_month):
    # binary_list = Binary.objects.filter(event_date__month=a_month,
    #                                     event_date__year=a_year)
    # binary_list = binary_list.order_by('-status_change_date')
    component_list = Component.objects.all()
    # event_list = EventLog.objects.all().order_by('-event_date')
    event_list = EventLog.objects.filter(event_date__month=a_month,
                                         event_date__year=a_year)
    event_list = event_list.order_by('-event_date')
    event_date_list = EventLog.objects.datetimes('event_date', 'day', order="DESC")

    upload_count_list = []
    for component in component_list:
        upload_count_list.append((component.name, len(Binary.objects.filter(upload_date__month=a_month,
                                                                            upload_date__year=a_year).filter(
            component=component))))
    modify_count_list = []
    for component in component_list:
        modify_count_list.append((component.name, len(Binary.objects.filter(status_change_date__month=a_month,
                                                                            status_change_date__year=a_year).filter(component=component))))
    context = {
        'event_list': event_list,
        'event_date_list': event_date_list,
        'component_list': component_list,
        'upload_count_list': upload_count_list,
        'modify_count_list': modify_count_list
    }
    return render(request, 'releases/activity_report.html', context)


def activity_report_date(request, a_year, a_month, a_day):
    # binary_list = Binary.objects.all().order_by('-status_change_date')
    component_list = Component.objects.all()
    event_list = EventLog.objects.filter(event_date__day=a_day,
                                         event_date__month=a_month,
                                         event_date__year=a_year)
    event_list = event_list.order_by('-event_date')
    event_date_list = EventLog.objects.datetimes('event_date', 'day', order="DESC")

    upload_count_list = []
    for component in component_list:
        upload_count_list.append((component.name, len(Binary.objects.filter(upload_date__day=a_day,
                                                                            upload_date__month=a_month,
                                                                            upload_date__year=a_year).filter(component=component))))
    modify_count_list = []
    for component in component_list:
        modify_count_list.append((component.name, len(Binary.objects.filter(status_change_date__day=a_day,
                                                                            status_change_date__month=a_month,
                                                                            status_change_date__year=a_year).filter(component=component))))
    context = {
        'event_list': event_list,
        'event_date_list': event_date_list,
        'component_list': component_list,
        'upload_count_list': upload_count_list,
        'modify_count_list': modify_count_list
    }
    return render(request, 'releases/activity_report.html', context)


# TODO:
def clear_unstable_binaries(request):
    binary_list = Binary.objects.filter(status="unstable")
    # for binary in binary_list:
    #     print binary.path
    remove_file(os.path.abspath(binary_list[0].path))

    return HttpResponseRedirect("/releases")


# TODO: Add user registration and user login features


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
            event_log = "Developer_Notes: {}".format(binary_object.notes)
            event_object = EventLog.objects.create(binary=binary_object,
                                                   component_name=component_obj.name,
                                                   status_change="upload",
                                                   event_log=event_log)
            print "New event: {}".format(event_object.event_log)

        return Response({'upload': 'success', 'binary_url': binary_url})

