from django.db.models.signals import post_migrate
from django.dispatch import receiver

from TestModel.models import *
import logging
import random
import time
from faker import Faker
from apscheduler.schedulers.background import BackgroundScheduler
import json

user_labels = ["学生党", "教师", "上班族", "无业"]
school = ["北大", "清华", "华科", "武大", "人大"]
goods_types = ['日用品', '服装', '数码用品', '食物']
goods_labels = ['引流品', '热卖品']
SCHEDULER = BackgroundScheduler()
SCHEDULER.start()
CRON = {"user": -1.0, "order": -1.0}
CRON_FUN = {}

def ch_name():
    faker = Faker("zh-CN")
    return faker.name()


def get_content():
    return {
        "goods_types": goods_types,
        "goods_labels": goods_labels
    }


def list_db(cls, offset, limit):
    list1 = cls.objects.order_by("id").reverse()[offset: offset+limit]
    return list(list1)


def add_user():
    user = MyTestUser(name=ch_name(), sex=random.choice(list(SexEm)).value,
                      status=random.choice(list(UserStatusEm)[:-1]).value,
                      labels=random.choice(user_labels), age=random.randint(16, 70),
                      school=random.choice(school))
    user.save()
    print("=-------->>>")
    logging.info("add_user：{}".format(user.uuid))


def add_goods(dd):
    user = random_user(MyTestUser, UserStatusEm.DELETE.value)
    MyTestGood.add(**dd, custom_id=user.uuid, custom_name=user.name, status=GoodStatusEm.ONLINE.value).save()

def random_user(cls, status):
    total = cls.objects.filter().exclude(status=status).count()
    offset = random.randint(0, total - 1)
    users = cls.objects.filter().exclude(status=status)[offset: offset + 1]
    return users[0]


def add_order():
    user = random_user(MyTestUser, UserStatusEm.DELETE.value)
    good = random_user(MyTestGood, GoodStatusEm.DELETE.value)
    price = random.randint(20, 1000)
    flag = random.randint(0, 9)
    if flag == 8:
        cur_time = time.time() - random.randint(100, 200)
    elif flag == 9:
        cur_time = time.time() - random.randint(200, 1000)
    else:
        cur_time = time.time() - random.randint(0, 100)
    order = MyTestOrder.add(user_id=user.uuid, status=OrderStatusEm.CREATED.value,
                    price=price, good_id=good.uuid, occur_time=cur_time)
    order.save()
    logging.info("add_order：{}".format(order.uuid))


def add_schedule(target, interval_sec, func):
    if not interval_sec:
        datas = MyTestSchedule.objects.all()
        if len(datas) < 1:
            return CRON
        for d in datas:
            if d.type not in CRON_FUN:
                continue
            CRON[d.type] = d.seconds
            set_schedule(d.type, CRON_FUN[d.type], d.seconds)
        return CRON
    interval_sec_f = float(interval_sec)
    MyTestSchedule.objects.filter(type=target).delete()
    MyTestSchedule(type=target, seconds=interval_sec_f).save()
    set_schedule(target, func, interval_sec_f)
    CRON[target] = interval_sec_f
    return CRON


def set_schedule(target, func, interval_sec):
    job = SCHEDULER.get_job(target)
    if job:
        job.remove()
    SCHEDULER.add_job(func, trigger='interval', id=target, seconds=float(interval_sec))


CRON_FUN = {"user": add_user, "order": add_order}
add_schedule(None, None, None)
