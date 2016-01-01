from django.db import models

# Create your models here.

class Server(models.Model):
  area = models.CharField(max_length=50, blank=True)
  ip = models.CharField(max_length=50)
  remark = models.CharField(max_length=50, blank=True)

  def __unicode__(self):
    return self.ip
