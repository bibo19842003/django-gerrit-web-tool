from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from server.models import Server
from gerrit.models import User, Port
import commands
# Create your views here.

def index(request):
  return render_to_response('index.html')

def ct_l_p(request):
  ip = Server.objects.all().order_by('ip')
  user = User.objects.all().order_by('name')
  port = Port.objects.all().order_by('number')

  if ( (request.GET.get('s-ip') != None) and (request.GET.get('g-user') != None) and (request.GET.get('g-port') != None) ):
    s_ip = request.GET.get('s-ip')
    g_user = request.GET.get('g-user')
    g_port = request.GET.get('g-port')

    if request.GET.has_key("fc"):
      run_string = "ssh -p " + g_port + " " + g_user + "@" + s_ip + " gerrit flush-caches"
    if request.GET.has_key("sc"):
      run_string = "ssh -p " + g_port + " " + g_user + "@" + s_ip + " gerrit show-caches"
    if request.GET.has_key("scon"):
      run_string = "ssh -p " + g_port + " " + g_user + "@" + s_ip + " gerrit show-connections"
    if request.GET.has_key("sq"):
      run_string = "ssh -p " + g_port + " " + g_user + "@" + s_ip + " gerrit show-queue"

    run_command = commands.getstatusoutput(run_string)
    shows = run_command
    return render_to_response('command_tool_less_para.html', {'ip': ip, 'user': user, 'port':port, 'shows':shows,})

  else:
    return render_to_response('command_tool_less_para.html', {'ip': ip, 'user': user, 'port':port,})

def ct_m_p(request):
  ip = Server.objects.all().order_by('ip')
  user = User.objects.all().order_by('name')
  port = Port.objects.all().order_by('number')

  if ( (request.GET.get('s-ip') != None) and (request.GET.get('g-user') != None) and (request.GET.get('g-port') != None) ):
    s_ip = request.GET.get('s-ip')
    g_user = request.GET.get('g-user')
    g_port = request.GET.get('g-port')

    username = request.GET.get('username')

    if request.GET.has_key("ls"):
      run_string = "ssh -p " + g_port + " " + g_user + "@" + s_ip + " gerrit ls-groups -u " + username
    if request.GET.has_key("ai"):
      run_string = "ssh -p " + g_port + " " + g_user + "@" + s_ip + " gerrit set-account" + username + " --inactive --delete-ssh-key -ALL "

    run_command = commands.getstatusoutput(run_string)
    shows = run_command
    return render_to_response('command_tool_more_para.html', {'ip': ip, 'user': user, 'port':port, 'shows':shows,})

  else:
    return render_to_response('command_tool_more_para.html', {'ip': ip, 'user': user, 'port':port,})

  

