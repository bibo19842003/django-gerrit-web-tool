from django.db import models

# Create your models here.

class Handler(models.Model):
  handler = models.CharField(max_length=20)

  def __str__(self):
    return self.handler


class ListSort(models.Model):
  list_sort = models.CharField(max_length=20)

  def __str__(self):
    return self.list_sort


class ListStatus(models.Model):
  list_status = models.CharField(max_length=20)

  def __str__(self):
    return self.list_status


class WorkList(models.Model):
  creator = models.CharField(max_length=20)
  create_time = models.CharField(max_length=30, null=True, blank=True)
  descripe = models.CharField(max_length=100)
  list_num = models.CharField(max_length=20)
  list_status = models.CharField(max_length=20, null=True, blank=True)
  list_sort = models.CharField(max_length=20, null=True, blank=True)
  handler = models.CharField(max_length=20, null=True, blank=True)
  handle_begin = models.CharField(max_length=30, null=True, blank=True)
  wait_time = models.CharField(max_length=30, null=True, blank=True)
  handle_end = models.CharField(max_length=30, null=True, blank=True)
  handle_time = models.CharField(max_length=30, null=True, blank=True)
  list_time = models.CharField(max_length=30, null=True, blank=True)

  def __str__(self):
    return '%s %s %s %s %s %s %s %s %s %s %s %s' % (self.creator, self.create_time, self.descripe, self.list_num, self.list_status, self.list_sort, self.handler, self.handle_begin, self.wait_time, self.handle_end, self.handle_time, self.list_time)
