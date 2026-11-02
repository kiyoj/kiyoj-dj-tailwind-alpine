from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view(), name='post_index'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('post/search', views.PostList.as_view(), name='post_search'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/<int:pk>/delete/', views.PostDelete.as_view(), name='post_delete'),
    path('post/add/', views.PostCreate.as_view(), name='post_add'),
    path('post/<int:pk>/update/', views.PostUpdate.as_view(), name='post_update'),
    path('comment/<int:pk>/', views.CommentFormView.as_view(), name='post_comment_form'),
    path('comment/<int:pk>/off/', views.post_comment_off, name='post_comment_off'),
    path('comment/<int:pk>/on/', views.post_comment_on, name='post_comment_on'),
    path('bbs/', views.BbsIndex.as_view(), name='bbs_index'),
	path('bbs/search', views.BbsIndex.as_view(), name='bbs_search'),
    path('bbs/<int:pk>/', views.BbsListView.as_view(), name='bbs_detail'),
    path('bbs/add/', views.BbsCreate.as_view(), name='bbs_add'),
    path('bbs/<int:pk>/update/', views.BbsUpdate.as_view(), name='bbs_update'),
    path('bbs/<int:pk>/off/', views.bbs_comment_off, name='bbs_comment_off'),
    path('bbs/<int:pk>/on/', views.bbs_comment_on, name='bbs_comment_on'),

]
