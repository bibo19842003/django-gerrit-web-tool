from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from server.models import Server, Gerritserver
from gerrit.models import User, Port, Branch, Owner, Qdownloadcommand
from django.contrib.auth.decorators import login_required
import commands, os, time, paramiko, xml.dom.minidom, json
# Create your views here.

def index(request):
  return render_to_response('index.html', context_instance=RequestContext(request))

def ct_l_p(request):
  ip = Server.objects.all().order_by('ip')
  name = User.objects.all().order_by('name')
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
      run_string = "ssh -p " + g_port + " " + g_user + "@" + s_ip + " gerrit show-queue -w"

    run_command = commands.getstatusoutput(run_string)
    shows = run_command
    return render_to_response('command_tool_less_para.html', {'ip': ip, 'name': name, 'port':port, 'shows':shows,}, context_instance=RequestContext(request))

  else:
    return render_to_response('command_tool_less_para.html', {'ip': ip, 'name': name, 'port':port,}, context_instance=RequestContext(request))

def ct_m_p(request):
  ip = Server.objects.all().order_by('ip')
  name = User.objects.all().order_by('name')
  port = Port.objects.all().order_by('number')

  if ( (request.GET.get('s-ip') != None) and (request.GET.get('g-user') != None) and (request.GET.get('g-port') != None) ):
    s_ip = request.GET.get('s-ip')
    g_user = request.GET.get('g-user')
    g_port = request.GET.get('g-port')

    username = request.GET.get('username')

    if request.GET.has_key("ls"):
      run_string = "ssh -p " + g_port + " " + g_user + "@" + s_ip + " gerrit ls-groups -u " + username
    if request.GET.has_key("ai"):
      run_string = "ssh -p " + g_port + " " + g_user + "@" + s_ip + " gerrit set-account " + username + " --inactive --delete-ssh-key -ALL "
    if request.GET.has_key("kt"):
      run_string = "ssh -p " + g_port + " " + g_user + "@" + s_ip + " kill " + username

    run_command = commands.getstatusoutput(run_string)
    shows = run_command
    return render_to_response('command_tool_more_para.html', {'ip': ip, 'name': name, 'port':port, 'shows':shows,}, context_instance=RequestContext(request))

  else:
    return render_to_response('command_tool_more_para.html', {'ip': ip, 'name': name, 'port':port,}, context_instance=RequestContext(request))


@login_required
def g_r(request):
  ip = Server.objects.all().order_by('ip')
  if request.GET.get('s-ip') != None:
    s_ip = request.GET.get('s-ip')
    if s_ip =="":
      return render_to_response('gerrit/gerritrestart/gerritrestart.html', {'ip': ip,}, context_instance=RequestContext(request))

    if request.method == "GET":
      g = str(Gerritserver.objects.filter(gerrit_ip__ip=s_ip)[0])
      g_ip = g.split()[0] 
      g_user = g.split()[1]
      g_d_ssh_p = int(g.split()[2])
      g_mail_to = g.split()[4]
      g_reviewsite = g.split()[6]
      g_sshkey = g.split()[7]

      gerrit_restart_run = "cd " + g_reviewsite + ";bin/gerrit.sh restart"
      pkey_file = g_sshkey + '/id_rsa'
      key = paramiko.RSAKey.from_private_key_file(pkey_file)
      s = paramiko.SSHClient()
      s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      s.load_system_host_keys()
      s.connect(hostname=g_ip,username=g_user, port=g_d_ssh_p, pkey=key)
      stdin,stout,stderr=s.exec_command(gerrit_restart_run)
      filedate = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
      runuser =str(request.user)
      restartlogpath = os.path.dirname(os.path.dirname(__file__)) + '/static/log/gerrit/gerritrestart/'
      logrestart = restartlogpath + filedate + '-' + runuser + '-' + g_ip + '.txt'
      restartcontent = filedate + '-' + runuser + '-' + g_ip
      f = open(logrestart ,'w')
      f.write(restartcontent)
      f.write('\n')
      f.write(stout.read())
      f.close()
      s.close()

      return render_to_response('gerrit/gerritrestart/gerritrestartok.html', {'ip': ip,}, context_instance=RequestContext(request))

  return render_to_response('gerrit/gerritrestart/gerritrestart.html', {'ip': ip,}, context_instance=RequestContext(request))


def g_r_log(request):
  path = os.path.dirname(os.path.dirname(__file__)) + '/static/log/gerrit/gerritrestart'
  filenames = os.listdir(path)
  filenames.sort(reverse = True)
  return render_to_response('gerrit/gerritrestart/gerritrestartlog.html', {'filenames': filenames,}, context_instance=RequestContext(request))


def c_b(request):
  ip = Server.objects.all().order_by('ip')

  if ( (request.GET.get('s-ip') != None) and (request.GET.get('manifestname') != None) and (request.GET.get('tagname') != None) and (request.GET.get('obname') != None) and (request.GET.get('nbname') != None) ):
    s_ip = request.GET.get('s-ip')
    if s_ip =="":
      return render_to_response('gerrit/createbranch/createbranch.html', {'ip': ip,}, context_instance=RequestContext(request))

    manifestname = request.GET.get('manifestname')
    tagname = request.GET.get('tagname')
    obname = request.GET.get('obname')
    nbname = request.GET.get('nbname')

    if request.method == "GET":
      g = str(Gerritserver.objects.filter(gerrit_ip__ip=s_ip)[0])
      g_g_ssh = g.split()[3]
      g_g_user = g.split()[8]
      runuser =str(request.user)

    workspace = os.path.dirname(os.path.dirname(__file__)) + '/common/createbranch'
    os.system(workspace + "/hi.sh %s %s %s %s %s %s %s %s %s %s" %(manifestname, tagname, obname, nbname, s_ip, g_g_user, g_g_ssh, os.path.dirname(os.path.dirname(__file__)), workspace, runuser))

    return render_to_response('gerrit/createbranch/createbranchok.html', {'ip': ip,}, context_instance=RequestContext(request))
  else:
    return render_to_response('gerrit/createbranch/createbranch.html', {'ip': ip,}, context_instance=RequestContext(request))


def c_b_log(request):
  path = os.path.dirname(os.path.dirname(__file__)) + '/static/log/gerrit/createbranch'
  filenames = os.listdir(path)
  filenames.sort(reverse = True)
  return render_to_response('gerrit/createbranch/createbranchlog.html', {'filenames': filenames,}, context_instance=RequestContext(request))


def q_b(request):
  branch = Branch.objects.all().order_by('branch')
  owner = Owner.objects.all().order_by('owner')
  if ( (request.GET.get('b-branch') != None) and (request.GET.get('b-owner') != None)):
    qbranch = request.GET.get('b-branch')
    qowner = request.GET.get('b-owner')
    qdownloadcommand = Qdownloadcommand.objects.filter(branch__branch__icontains=qbranch,owner__owner__icontains=qowner)
    return render_to_response('gerrit/querybranch/branch.html', {'branch': branch, 'owner': owner, 'qdownloadcommand': qdownloadcommand,}, context_instance=RequestContext(request))
  else:
    return render_to_response('gerrit/querybranch/branch.html', {'branch': branch, 'owner': owner,}, context_instance=RequestContext(request))


@login_required
def g_c(request):
  ip = Server.objects.all().order_by('ip')
  if ( (request.GET.get('s-ip') != None) and (request.GET.get('projectname') != None) ):
    s_ip = request.GET.get('s-ip')
    if s_ip =="":
      return render_to_response('gerrit/gitgc/gitgc.html', {'ip': ip,}, context_instance=RequestContext(request))

    projectname = request.GET.get('projectname')

    if request.method == "GET":
      g = str(Gerritserver.objects.filter(gerrit_ip__ip=s_ip)[0])
      g_ip = g.split()[0]
      g_user = g.split()[1]
      g_d_ssh_p = int(g.split()[2])
      g_mail_to = g.split()[4]
      g_project_path = g.split()[5]
      g_sshkey = g.split()[7]

      project_path = g_project_path + '/' + projectname

      filedate = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
      runuser =str(request.user)
      gitgclogpath = os.path.dirname(os.path.dirname(__file__)) + '/static/log/gerrit/gitgc/'
      loggitgc = gitgclogpath + filedate + '-' + runuser + '-' + g_ip + '.txt'
      gitgccontent = filedate + '-' + runuser + '-' + g_ip

      git_gc_run = "cd " + project_path + " && git gc >> " + loggitgc + " 2>&1 && echo " + projectname + " > " + loggitgc
      pkey_file = g_sshkey + '/id_rsa'
      key = paramiko.RSAKey.from_private_key_file(pkey_file)
      s = paramiko.SSHClient()
      s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      s.load_system_host_keys()
      s.connect(hostname=g_ip,username=g_user, port=g_d_ssh_p, pkey=key)
      stdin,stdout,stderr=s.exec_command(git_gc_run)

      return render_to_response('gerrit/gitgc/gitgcok.html', {'ip': ip,}, context_instance=RequestContext(request))

  return render_to_response('gerrit/gitgc/gitgc.html', {'ip': ip,}, context_instance=RequestContext(request))


def g_c_log(request):
  path = os.path.dirname(os.path.dirname(__file__)) + '/static/log/gerrit/gitgc'
  filenames = os.listdir(path)
  filenames.sort(reverse = True)
  return render_to_response('gerrit/gitgc/gitgclog.html', {'filenames': filenames,}, context_instance=RequestContext(request))


@login_required
def p_c(request):
  ip = Server.objects.all().order_by('ip')
  outfile = os.path.dirname(os.path.dirname(__file__)) + '/static/log/gerrit/projectchildren/project.log'

  if ( (request.GET.get('s-ip') != None) and (request.GET.get('projectname') != None) ):
    s_ip = request.GET.get('s-ip')
    projectname = request.GET.get('projectname').replace("/", "%2F")

    g = str(Gerritserver.objects.filter(gerrit_ip__ip=s_ip)[0])
    g_http = g.split()[3]
    g_path = g.split()[6]
    g_user = g.split()[8]
    g_pass = g.split()[9]

    gerrit_config = g_path + "/etc/gerrit.config"
    auth = commands.getstatusoutput("git config -f /home/bibo/house/work/review_site/etc/gerrit.config --get auth.gitBasicAuthPolicy")[1]
    if auth == "http":
      api_command = "curl --basic --user " + g_user + ":" + g_pass + " http://" + s_ip + ":" + g_http + "/a/projects/" + projectname + "/children > " + outfile + "; sed -i '1d' " + outfile
    else:
      api_command = "curl --user " + g_user + ":" + g_pass + " http://" + s_ip + ":" + g_http + "/a/projects/" + projectname + "/children > " + outfile + "; sed -i '1d' " + outfile
    commands.getstatusoutput(api_command)
    count = len(open(outfile, 'rU').readlines())
    if count == 1:
      return render_to_response('gerrit/projectchildren/project_is_not_exist.html', {'ip': ip,}, context_instance=RequestContext(request))

    jsondata = open(outfile)
    data = json.load(jsondata)

    tvalues = []
    for line in data:
      gtvalues = line.values()
      tvalues.append(gtvalues)

    jsondata.close

    return render_to_response('gerrit/projectchildren/list.html', {'ip': ip, 'tvalues': tvalues }, context_instance=RequestContext(request))
  else:
    return render_to_response('gerrit/projectchildren/empty.html', {'ip': ip,}, context_instance=RequestContext(request))


def u_g(request):
  ip = Server.objects.all().order_by('ip')
  outfile = os.path.dirname(os.path.dirname(__file__)) + '/static/log/gerrit/listusergroup/group.log'

  if ( (request.GET.get('s-ip') != None) and (request.GET.get('user') != None) ):
    s_ip = request.GET.get('s-ip')
    user = request.GET.get('user').replace("/", "%2F")

    g = str(Gerritserver.objects.filter(gerrit_ip__ip=s_ip)[0])
    g_http = g.split()[3]
    g_path = g.split()[6]
    g_user = g.split()[8]
    g_pass = g.split()[9]

    gerrit_config = g_path + "/etc/gerrit.config"
    auth = commands.getstatusoutput("git config -f /home/bibo/house/work/review_site/etc/gerrit.config --get auth.gitBasicAuthPolicy")[1]
    if auth == "http":
      api_command = "curl --basic --user " + g_user + ":" + g_pass + " http://" + s_ip + ":" + g_http + "/a/accounts/" + user + "/groups > " + outfile + "; sed -i '1d' " + outfile
    else:
      api_command = "curl --user " + g_user + ":" + g_pass + " http://" + s_ip + ":" + g_http + "/a/accounts/" + user + "/groups > " + outfile + "; sed -i '1d' " + outfile
    commands.getstatusoutput(api_command)
    count = len(open(outfile, 'rU').readlines())
    if count == 0:
      return render_to_response('gerrit/listusergroup/user_is_not_exist.html', {'ip': ip,}, context_instance=RequestContext(request))

    jsondata = open(outfile)
    data = json.load(jsondata)

    tvalues = []
    for line in data:
      gtvalues = line.values()
      tvalues.append(gtvalues)

    jsondata.close

    return render_to_response('gerrit/listusergroup/list.html', {'ip': ip, 'tvalues': tvalues }, context_instance=RequestContext(request))
  else:
    return render_to_response('gerrit/listusergroup/empty.html', {'ip': ip,}, context_instance=RequestContext(request))


def g_t(request):
  ip = Server.objects.all().order_by('ip')
  outfile = os.path.dirname(os.path.dirname(__file__)) + '/static/log/gerrit/gerrittask/task.log'

  if (request.GET.get('s-ip') != None):
    s_ip = request.GET.get('s-ip')

    g = str(Gerritserver.objects.filter(gerrit_ip__ip=s_ip)[0])
    g_http = g.split()[3]
    g_path = g.split()[6]
    g_user = g.split()[8]
    g_pass = g.split()[9]

    gerrit_config = g_path + "/etc/gerrit.config"
    auth = commands.getstatusoutput("git config -f /home/bibo/house/work/review_site/etc/gerrit.config --get auth.gitBasicAuthPolicy")[1]

    if request.GET.has_key("search"):
      if auth == "http":
        api_command = "curl --basic --user " + g_user + ":" + g_pass + " http://" + s_ip + ":" + g_http + "/a/config/server/tasks > " + outfile + "; sed -i '1d' " + outfile
      else:
        api_command = "curl --user " + g_user + ":" + g_pass + " http://" + s_ip + ":" + g_http + "/a/config/server/tasks > " + outfile + "; sed -i '1d' " + outfile
      commands.getstatusoutput(api_command)
      count = len(open(outfile, 'rU').readlines())

      jsondata = open(outfile)
      data = json.load(jsondata)

      tkeys = []
      for line in data:
        tkeys = line.keys()
        break

      tvalues = []
      for line in data:
        gtvalues = line.values()
        tvalues.append(gtvalues)

      jsondata.close

      return render_to_response('gerrit/gerrittask/list.html', {'ip': ip, 'tvalues': tvalues, 'tkeys': tkeys }, context_instance=RequestContext(request))

    if request.GET.has_key("kill"):
      radioid = request.GET.get('radioid')
      if radioid != None:
        if auth == "http":
          api_command = "curl -X DELETE --basic --user " + g_user + ":" + g_pass + " http://" + s_ip + ":" + g_http + "/a/config/server/tasks/" + radioid + " ; curl --basic --user " + g_user + ":" + g_pass + " http://" + s_ip + ":" + g_http + "/a/config/server/tasks > " + outfile + "; sed -i '1d' " + outfile
        else:
          api_command = "curl -X DELETE --user " + g_user + ":" + g_pass + " http://" + s_ip + ":" + g_http + "/a/config/server/tasks/" + radioid + " ; curl --user " + g_user + ":" + g_pass + " http://" + s_ip + ":" + g_http + "/a/config/server/tasks > " + outfile + "; sed -i '1d' " + outfile
        commands.getstatusoutput(api_command)
        count = len(open(outfile, 'rU').readlines())

        jsondata = open(outfile)
        data = json.load(jsondata)

        tkeys = []
        for line in data:
          tkeys = line.keys()
          break

        tvalues = []
        for line in data:
          gtvalues = line.values()
          tvalues.append(gtvalues)

        jsondata.close

        return render_to_response('gerrit/gerrittask/list.html', {'ip': ip, 'tvalues': tvalues, 'tkeys': tkeys }, context_instance=RequestContext(request))
      else:
        return render_to_response('gerrit/gerrittask/empty.html', {'ip': ip,}, context_instance=RequestContext(request))
  else:
    return render_to_response('gerrit/gerrittask/empty.html', {'ip': ip,}, context_instance=RequestContext(request))


@login_required
def c_p(request):
  runuser =str(request.user)
  ip = Server.objects.all().order_by('ip')
  outfile = os.path.dirname(os.path.dirname(__file__)) + '/static/log/gerrit/createproject/create.log'
  if ( (request.GET.get('s-ip') != None) and (request.GET.get('parentproject') != None) and (request.GET.get('projectname') != None) ):
    s_ip = request.GET.get('s-ip')
    if s_ip =="":
      return render_to_response('gerrit/createproject/createproject.html', {'ip': ip,}, context_instance=RequestContext(request))

    parentproject = request.GET.get('parentproject').replace("/", "%2F")
    if parentproject =="":
      return render_to_response('gerrit/createproject/createproject.html', {'ip': ip,}, context_instance=RequestContext(request))

    g = str(Gerritserver.objects.filter(gerrit_ip__ip=s_ip)[0])
    g_ssh_port = g.split()[2]
    g_http = g.split()[3]
    g_path = g.split()[6]
    g_user = g.split()[8]
    g_pass = g.split()[9]

    gerrit_config = g_path + "/etc/gerrit.config"
    auth = commands.getstatusoutput("git config -f /home/bibo/house/work/review_site/etc/gerrit.config --get auth.gitBasicAuthPolicy")[1]
    if auth == "http":
      api_command = "curl --basic --user " + g_user + ":" + g_pass + " http://" + s_ip + ":" + g_http + "/a/projects/" + parentproject + " > " + outfile + "; sed -i '1d' " + outfile
    else:
      api_command = "curl --user " + g_user + ":" + g_pass + " http://" + s_ip + ":" + g_http + "/a/projects/" + parentproject + " > "  + outfile + "; sed -i '1d' " + outfile
    commands.getstatusoutput(api_command)
    count = len(open(outfile, 'rU').readlines())
    if count == 0:
      return render_to_response('gerrit/createproject/parentproject_is_not_exist.html', {'ip': ip,}, context_instance=RequestContext(request))

    projectname = request.GET.get('projectname')
    if projectname =="":
      return render_to_response('gerrit/createproject/createproject.html', {'ip': ip,}, context_instance=RequestContext(request))

    workspace = os.path.dirname(os.path.dirname(__file__)) + '/common/createproject'
    runtime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    print(projectname)
    for project in projectname.split():
      os.system(workspace + "/createproject.sh %s %s %s %s %s %s %s %s" %(g_ssh_port, g_user, s_ip, project, parentproject, runtime, runuser, os.path.dirname(os.path.dirname(__file__))))

    return render_to_response('gerrit/createproject/createprojectok.html', {'ip': ip,}, context_instance=RequestContext(request))

  return render_to_response('gerrit/createproject/createproject.html', {'ip': ip,}, context_instance=RequestContext(request))


def c_p_log(request):
  path = os.path.dirname(os.path.dirname(__file__)) + '/static/log/gerrit/createproject'
  filenames = os.listdir(path)
  filenames.sort(reverse = True)
  return render_to_response('gerrit/createproject/createprojectlog.html', {'filenames': filenames,}, context_instance=RequestContext(request))

