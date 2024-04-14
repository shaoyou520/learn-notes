
from django.contrib import admin
from django.urls import path
from . import views
from . import service
from TestModel.models import *

urlpatterns = [
    path('goods', views.list_view, {'cls': MyTestGood, 'page': 'goods'}),
    path('user', views.list_view, {'cls': MyTestUser, 'page': 'user'}),
    path('order', views.list_view, {'cls': MyTestOrder, 'page': 'order'}),
    path('cron_user', views.my_cron, {'target': 'user', 'func': service.add_user}),
    path('cron_order', views.my_cron, {'target': 'order', 'func': service.add_order}),
    # path('schedule', views.schedule),
    path('goods/add', views.add_goods_view),
    path('', views.my_cron),
]
