from django.db import models

# Create your models here.

class User(models.Model):
  name = models.CharField(max_length=10)

#  def __unicode__(self):
#    return self.name

class Port(models.Model):
  number = models.CharField(max_length=5)

