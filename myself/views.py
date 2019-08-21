from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader, Context
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
# Create your views here.


@login_required
def infor_list(request):

  usergroups = request.user.groups.all()
  print(usergroups)

  return render(request, 'myself/myself.html', {'usergroups': usergroups,})







