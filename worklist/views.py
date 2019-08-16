from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader, Context
from worklist.models import Handler, ListSort, ListStatus, WorkList
from django.contrib.auth.decorators import login_required
import subprocess, os, time, paramiko, xml.dom.minidom, json
from datetime import datetime
from django.contrib.auth.models import User, Group
# Create your views here.



def list_queryxxx(request):
  return render(request, 'index.html')


# @login_required
def list_query(request):
  handler = Handler.objects.all().order_by('handler')
  list_sort = ListSort.objects.all().order_by('list_sort')
  list_status = ListStatus.objects.all().order_by('list_status')
  if ( (request.GET.get('w-handler') != None) and (request.GET.get('w-list-sort') != None) and (request.GET.get('w-list-status') != None) ):
    qhandler = request.GET.get('w-handler')
    qlist_sort = request.GET.get('w-list-sort')
    qlist_status = request.GET.get('w-list-status')
#    worklist = WorkList.objects.filter(handler__icontains=qhandler,list_sort__icontains=qlist_sort,list_status__icontains=qlist_status)
    worklist = WorkList.objects.filter(list_sort__icontains=qlist_sort,list_status__icontains=qlist_status)
    return render(request, 'worklist/work_list.html', {'handler': handler, 'list_sort': list_sort, 'list_status': list_status, 'worklist': worklist,})
  else:
    return render(request, 'worklist/work_list.html', {'handler': handler, 'list_sort': list_sort, 'list_status': list_status,})



@login_required
def list_create(request):
  list_sort = ListSort.objects.all().order_by('list_sort')

  if ( (request.GET.get('w-description') != None) and (request.GET.get('w-list-sort') != None) ):
    descripe = request.GET.get('w-description')
    qlist_sort = request.GET.get('w-list-sort')

    creator = request.user
    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    list_num = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
    list_status = "wait for handle"
    
    createlist = WorkList(creator=creator, create_time=create_time, descripe=descripe, list_num=list_num, list_sort=qlist_sort, list_status=list_status)
    createlist.save()

    return render(request, 'worklist/create_list.html')

  else:

    return render(request, 'worklist/create_list.html', {'list_sort': list_sort,})



@login_required
def list_handle(request):
  list_status = ListStatus.objects.all().order_by('list_status')

  if (request.GET.get('w-list-status') != None):

    qlist_status = request.GET.get('w-list-status')

    if "querydata" in request.GET:
      worklist = WorkList.objects.filter(list_status__icontains=qlist_status)
      return render(request, 'worklist/handle_list.html', {'list_status': list_status, 'worklist': worklist,})

    if "listaccept" in request.GET:
      radioid = request.GET.get('radioid')
      if radioid != None:
        handler = str(request.user)
        handle_begin = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        WorkList.objects.filter(list_num=radioid).update(list_status="handling", handler=handler, handle_begin=handle_begin)

        create_time = WorkList.objects.filter(list_num=radioid)
        gg = str(create_time).split()[3] + " " + str(create_time).split()[4]
        create_time_a = datetime.strptime(gg,"%Y-%m-%d %H:%M:%S")
        handle_begin_a = datetime.strptime(handle_begin,"%Y-%m-%d %H:%M:%S")
        wait_time = handle_begin_a - create_time_a
        WorkList.objects.filter(list_num=radioid).update(wait_time=wait_time)

        worklist = WorkList.objects.filter(list_status__icontains=qlist_status)
        return render(request, 'worklist/handle_list.html', {'list_status': list_status, 'worklist': worklist,})
      else:
        worklist = WorkList.objects.filter(list_status__icontains=qlist_status)
        return render(request, 'worklist/handle_list.html', {'list_status': list_status, 'worklist': worklist,})

    if "listdone" in request.GET:
      radioid = request.GET.get('radioid')
      if radioid != None:
        handle_end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        WorkList.objects.filter(list_num=radioid).update(handle_end=handle_end, list_status="done")

        qs = WorkList.objects.filter(list_num=radioid)
        gg = str(qs).split()[3] + " " + str(qs).split()[4]
        hh = str(qs).split()[10] + " " + str(qs).split()[11]
        create_time_a = datetime.strptime(gg,"%Y-%m-%d %H:%M:%S")
        handle_begin_a = datetime.strptime(hh,"%Y-%m-%d %H:%M:%S")
        handle_end_a = datetime.strptime(handle_end,"%Y-%m-%d %H:%M:%S")
        list_time = handle_end_a - create_time_a
        handle_time = handle_end_a - handle_begin_a

        WorkList.objects.filter(list_num=radioid).update(list_time=list_time, handle_time=handle_time)
#        WorkList.objects.filter(list_num=radioid).update(list_time=list_time)

        worklist = WorkList.objects.filter(list_status__icontains=qlist_status)
        return render(request, 'worklist/handle_list.html', {'list_status': list_status, 'worklist': worklist,})
      else:
        worklist = WorkList.objects.filter(list_status__icontains=qlist_status)
        return render(request, 'worklist/handle_list.html', {'list_status': list_status, 'worklist': worklist,})

    else:
      worklist = WorkList.objects.filter(list_status__icontains=qlist_status)
      return render(request, 'worklist/handle_list.html', {'list_status': list_status, 'worklist': worklist,})

  else:
    return render(request, 'worklist/handle_list.html', {'list_status': list_status,})




