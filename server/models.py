from django.db import models

# Create your models here.

class Server(models.Model):
  area = models.CharField(max_length=50, blank=True)
  ip = models.CharField(max_length=50)
  remark = models.CharField(max_length=50, blank=True)

  def __str__(self):
    return self.ip


class Gerritserver(models.Model):
  gerrit_ip = models.OneToOneField(Server, on_delete=models.CASCADE)
  user = models.CharField(max_length=100)
  gerrit_ssh_port = models.CharField(max_length=100)
  gerrit_http_port = models.CharField(max_length=100)
  default_ssh_port = models.CharField(max_length=100)
  mail_to = models.CharField(max_length=100)
  project_path= models.CharField(max_length=100)
  reviewsite_path = models.CharField(max_length=100)
  sshkey_path = models.CharField(max_length=100)
  gerrit_user = models.CharField(max_length=100)
  gerrit_pass = models.CharField(max_length=100)

  def __str__(self):
    return '%s %s %s %s %s %s %s %s %s %s' % (self.gerrit_ip, self.user, self.gerrit_ssh_port, self.gerrit_http_port, self.mail_to, self.project_path, self.reviewsite_path, self.sshkey_path, self.gerrit_user, self.gerrit_pass)
