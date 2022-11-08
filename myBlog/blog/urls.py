from django.urls import path

from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('archive/', views.archive, name='archive'),
  path('archive/<str:category>/', views.category_list, name='category'),
  path('archive/<str:category>/<str:url_name>/', views.post_detail, name='post_detail'),
  path('about/', views.about, name='about'),
]