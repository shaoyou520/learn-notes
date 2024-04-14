from django.db import models
import uuid
from .modelem import *

class MyTestGood(models.Model):
    uuid = models.CharField(max_length=36, blank=True, null=True, editable=False, default=uuid.uuid4)
    type = models.CharField(max_length=12, blank=True, null=True)
    describe = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    labels = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=16, blank=True, null=True, choices=choices(GoodStatusEm))
    create_time = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    update_time = models.DateTimeField(blank=True, null=True, auto_now=True)
    create_user = models.CharField(max_length=36, blank=True, null=True)
    custom_id = models.CharField(max_length=36, blank=True, null=True)
    custom_name = models.CharField(max_length=64, blank=True, null=True)
    delete_time = models.DateTimeField(blank=True, null=True)

    @classmethod
    def add(cls, type, name, status, custom_id, custom_name, **kwargs):
        return MyTestGood(type=type, name=name, status=status, custom_id=custom_id,
                          custom_name=custom_name, describe=kwargs['describe'],
                          labels=kwargs['labels'], create_user=custom_id)

    class Meta:
        managed = False
        db_table = 'my_test_good'



class MyTestUser(models.Model):

    uuid = models.UUIDField(max_length=36, blank=True, null=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=64, blank=True, null=True)
    create_user = models.CharField(max_length=36, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True, auto_now=True)
    delete_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=16, blank=True, null=True, choices=choices(UserStatusEm))
    labels = models.CharField(max_length=255, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    sex = models.CharField(max_length=1, blank=True, null=True, choices=choices(SexEm))
    school = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'my_test_user'


class MyTestOrder(models.Model):
    uuid = models.CharField(max_length=36, blank=True, null=True, editable=False, default=uuid.uuid4)
    user_id = models.CharField(max_length=36, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True, auto_now=True)
    status = models.CharField(max_length=16, blank=True, null=True, choices=choices(OrderStatusEm))
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    good_id = models.CharField(max_length=36, blank=True, null=True)
    delete_time = models.DateTimeField(blank=True, null=True)
    occur_time = models.BigIntegerField(max_length=16, null=True)

    @classmethod
    def add(cls, user_id, status, price, good_id, occur_time, **kwargs):
        return MyTestOrder(user_id=user_id, status=status, price=price, good_id=good_id,
                           occur_time = occur_time)

    class Meta:
        managed = False
        db_table = 'my_test_order'

class Test(models.Model):
    name = models.CharField(max_length=20)

    @classmethod
    def add(cls, name, **kwargs):
        return Test(name=name)

    class Meta:
        managed = False
        db_table = 'test'


class MyTestSchedule(models.Model):
    type = models.CharField(max_length=255, blank=True, null=True)
    seconds = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'my_test_schedule'
