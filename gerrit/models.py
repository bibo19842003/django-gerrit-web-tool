from django.db import models

# Create your models here.

class User(models.Model):
  name = models.CharField(max_length=10)

#  def __str__(self):
#    return self.name

class Port(models.Model):
  number = models.CharField(max_length=5)

class Branch(models.Model):
  branch = models.CharField(max_length=50)

  def __str__(self):
    return self.branch

class Owner(models.Model):
  owner = models.CharField(max_length=50)

  def __str__(self):
    return self.owner

class Qdownloadcommand(models.Model):
  branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
  download_command = models.CharField(max_length=100)
  descripe = models.CharField(max_length=100)
  owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
  create_time = models.DateTimeField()

  def __str__(self):
    return '%s %s %s %s %s' % (self.branch, self.download_command, self.owner, self.descripe, self.create_time)
