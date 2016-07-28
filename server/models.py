from django.db import models

# Create your models here.

class Server(models.Model):
  area = models.CharField(max_length=50, blank=True)
  ip = models.CharField(max_length=50)
  user = models.CharField(max_length=100)
  gerrit_ssh = models.CharField(max_length=100)
  gerrit_http = models.CharField(max_length=100)
  default_ssh = models.CharField(max_length=100)
  mail_to = models.CharField(max_length=100)
  project_path= models.CharField(max_length=100)
  reviewsite_path = models.CharField(max_length=100)
  remark = models.CharField(max_length=50, blank=True)

  def __unicode__(self):
    return '%s %s %s %s %s %s %s' % (self.ip, self.user, self.default_ssh, self.gerrit_ssh, self.mail_to, self.project_path, self.reviewsite_path)
