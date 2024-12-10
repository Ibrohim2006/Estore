from django.urls import path
from .views import blog_view, blog_detail_view, tag_view

app_name = 'blog'
urlpatterns = [
    path('', blog_view, name='blog'),
    path('<str:slug>/', blog_detail_view, name='blog_detail'),
    path('tag/<str:slug>/', tag_view, name='tag_list'),
]
