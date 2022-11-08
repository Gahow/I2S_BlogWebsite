from django.db import models
from django.db.models.signals import pre_delete, post_save, post_init
from django.dispatch.dispatcher import receiver
from django.utils import timezone
from pathlib import Path
from urllib import parse
from zipfile import ZipFile

import os
import shutil
import zipfile

# Create your models here.

def get_post_path(instance, postname):
  path = 'blog/archive/%s/%s' % (instance.category, postname)
  return path

class Post(models.Model):
  title = models.CharField(max_length=100)
  category = models.CharField(max_length=100)
  url_name = models.CharField(max_length=100)
  publish_time = models.DateTimeField(default=timezone.now)
  introduction = models.TextField()
  body = models.FileField(upload_to=get_post_path)


@receiver(pre_delete, sender=Post)
def delete(sender, instance, **kwargs):
  shutil.rmtree('blog/archive/' + instance.category + '/' + instance.url_name)


def support_gbk(file: ZipFile):
  name_to_info = file.NameToInfo
  for name, info in name_to_info.copy().items():
    real_name = name.encode('cp437').decode('utf-8')
    if real_name != name:
      info.filename = real_name
      del name_to_info[name]
      name_to_info[real_name] = info
  return file

@receiver(post_save, sender=Post)
def unzip_file(sender, instance, **kwargs):
  # zip_path = instance.body.url[1:]
  zip_path = parse.unquote(instance.body.url[1:])
  zip_file_name = '.'.join(zip_path.split('/')[-1].split('.')[ : -1])
  to_path = 'blog/archive/' + instance.category + '/'

  file_list = os.listdir(to_path)
  if instance.url_name in file_list:
    shutil.rmtree(to_path + instance.url_name)

  # z = zipfile.ZipFile(zip_path, 'r')
  # z.extractall(path=to_path)
  with support_gbk(ZipFile(zip_path)) as zfp:
    zfp.extractall(path=to_path)
  ''' with zipfile.ZipFile(zip_path, 'r') as z:
    for f in z.namelist():
      filename = f.encode('cp437').decode('utf-8')
      print(filename)
      extracted_path = Path(z.extract(f, path=to_path))
      print(extracted_path)
      extracted_path.rename(to_path + filename) '''
  os.rename(to_path + zip_file_name, to_path + instance.url_name)
  # z.close()
  os.remove(zip_path)
