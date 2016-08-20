from django.db import models

# Create your models here.

class User(models.Model):
  name = models.CharField(max_length=10)

#  def __unicode__(self):
#    return self.name

class Port(models.Model):
  number = models.CharField(max_length=5)

class Branch(models.Model):
  branch = models.CharField(max_length=50)

  def __unicode__(self):
    return self.branch

class Owner(models.Model):
  owner = models.CharField(max_length=50)

  def __unicode__(self):
    return self.owner

class Qdownloadcommand(models.Model):
  branch = models.ForeignKey(Branch)
  download_command = models.CharField(max_length=100)
  descripe = models.CharField(max_length=100)
  owner = models.ForeignKey(Owner)
  create_time = models.DateTimeField()

  def __unicode__(self):
    return '%s %s %s %s %s' % (self.branch, self.download_command, self.owner, self.descripe, self.create_time)
