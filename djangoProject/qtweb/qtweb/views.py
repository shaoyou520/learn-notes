from django.http import HttpResponse
from django.shortcuts import render
from .service import *

DEFAULT_PAGE_NO = 0
DEFAULT_PAGE_SIZE = 50


def list_view(request, cls, page):
    page_no = DEFAULT_PAGE_NO if not request.GET.get("pageNo") else request.GET.get("pageNo")
    page_size = DEFAULT_PAGE_SIZE if not request.GET.get("pageSize") else request.GET.get("pageSize")
    return render(request, page + '.html', {"datas": list_db(cls, page_no * page_size, page_size),
                                            "pageSize": page_size,
                                            "pageNo": page_no})


def add_goods_view(request):
    if request.method == "POST":
        add_goods({
            "name": request.POST.get("name"),
            "type": request.POST.get("type"),
            "labels": ",".join(request.POST.getlist("labels", [])),
            "describe": request.POST.get("describe")
        })


def index(request):
    page = request.GET.get('view')
    if not page:
        page = 'goods'
    return render(request, 'index.html', {'page': page})

# def schedule(request):
#     job = SCHEDULER.get_job(target)
#     return render(request, 'schedule.html', {'page': })


def my_cron(request, target=None, func=None):
    interval_sec = request.GET.get("interval_sec")
    cron = add_schedule(target, interval_sec, func)
    return render(request, 'schedule.html', cron)

