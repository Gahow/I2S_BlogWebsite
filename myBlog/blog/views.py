from django.shortcuts import render
import re
import markdown
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
import os
import requests
import random
from datetime import date

from .models import Post

# Create your views here.

class Catergory:
  name = ''
  count = 0
  def __init__(self, name, count):
    self.name = name
    self.count = count


class History:
  title = ''
  picurl = ''
  year = ''
  def __init__(self, title, picurl, year):
    self.title = title
    self.picurl = picurl
    self.year = year


class News:
  title = ''
  url = ''
  def __init__(self, title, url):
    self.title = title
    self.url = url


def home(request):
  history = None
  today_str = date.today().strftime('%m%d')
  request_url = 'http://dh.ylapi.cn/today_his/query.u?uid=12342&appkey=1448bc18c3d82286aefea990553bb8e8&date=' + today_str
  item = requests.get(request_url, timeout=30)
  if item and 'datas' in item.json():
    data = item.json()['datas']
    lis = []
    for d in data:
      if 'img' in d:
        lis.append(d)
    random_number = random.randint(0, len(lis) - 1)
    choice = lis[random_number]
    history = History(choice['title'], choice['img'], choice['year'])


  news_list = []
  news_url = 'https://way.jd.com/jisuapi/get?channel=科技&num=5&start=0&appkey=da39dce4f8aa52155677ed8cd23a6470'
  item = requests.get(news_url, timeout=30)
  if item and 'result' in item.json() and 'result' in item.json()['result']:
    data = item.json()['result']['result']['list']
    for i in range(5):
      news_list.append(News(data[i]['title'], data[i]['weburl']))


  latest_posts = Post.objects.order_by('-publish_time')[:2]
  for post in latest_posts:
    post.publish_time = post.publish_time.strftime('%Y-%m-%d')
  context = {
    'history_today': history,
    'news': news_list,
    'latest_posts': latest_posts,
  }
  return render(request, 'home/home.html', context)


def archive(request):
  posts = Post.objects.order_by('-publish_time')
  categorys = {}
  for post in posts:
    category = post.category
    if category not in categorys:
      categorys[category] = 0
    categorys[category] += 1
    post.publish_time = post.publish_time.strftime('%Y.%m.%d')

  category_list = []
  for name in categorys:
    category_list.append(Catergory(name, categorys[name]))
  
  context = {
    'latest_posts': posts[ : 1],
    'posts': posts,
    'categorys': category_list
  }
  return render(request, 'archive/archive.html', context)


def category_list(request, category):
  posts = Post.objects.order_by('-publish_time')
  post_list = []
  categorys = {}
  for post in posts:
    if post.category == category:
      post_list.append(post)
    cur_category = post.category
    if cur_category not in categorys:
      categorys[cur_category] = 0
    categorys[cur_category] += 1
    post.publish_time = post.publish_time.strftime('%Y.%m.%d')

  category_list = []
  for name in categorys:
    category_list.append(Catergory(name, categorys[name]))
  
  context = {
    'latest_posts': posts[ : 1],
    'posts': post_list,
    'categorys': category_list
  }
  return render(request, 'archive/category.html', context)


def post_detail(request, category, url_name):
  md_body = ""

  dir_path = 'blog/archive/' + category + '/' + url_name + '/'
  all_files = os.listdir(dir_path)
  for file in all_files:
    if file.split('.')[-1] == 'md':
      with open(dir_path + file, encoding='utf-8') as f:
        md_body = f.read()
      break

  change_picture = lambda matched: '<img src="/static/' + category + '/' + url_name + '/' + matched.group(1) + '" class="img-responsive center-block" style="max-width:100%;max-height:100%;width:auto;height:auto;">' 

  md_body = re.sub(r'<img src\s*=\s*\"(.+\..+)\"\s*/{0,1}>', change_picture, md_body)

  md_uti = markdown.Markdown(
    extensions=[
      'markdown.extensions.extra',
      'markdown.extensions.codehilite',
      'mdx_math',
      TocExtension(slugify=slugify),
    ]
  )
  md_uti.convert(md_body)
  level = 7
  for item in md_uti.toc_tokens:
    level = min(level, item['level'])

  md_uti = markdown.Markdown(
    extensions=[
      'markdown.extensions.extra',
      'markdown.extensions.codehilite',
      'mdx_math',
      TocExtension(slugify=slugify, baselevel=-level + 2, toc_depth=2),
    ]
  )
  md_body = md_uti.convert(md_body)

  return render(request, 'archive/post_detail.html', {'body': md_body, 'toc': md_uti.toc})


def about(request):
  return render(request, 'about/about.html')