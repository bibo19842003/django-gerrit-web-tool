from django.shortcuts import render
from django.shortcuts import HttpResponse
import psutil

# Create your views here.
# http://www.cnblogs.com/fiyajim/p/5668457.html
# http://www.javafeng.com/index.php/archives/420/

def m_mem(request):
    m = psutil.virtual_memory()
    total_mem = m.total / 1024 / 1024
    used_mem_percentage = m.percent
    free_mem_percentage = 100 - m.percent
    return render(request, 'monitor/mem/mem.html', {"total_mem":total_mem,"used_mem": used_mem_percentage,"free_mem":free_mem_percentage})


def m_cpu(request):
    a = psutil.cpu_times_percent()
    user_percentage = a.user
    system_percentage = a.system
    return render(request, 'monitor/cpu/cpu.html', {"user": user_percentage,"system":system_percentage})

