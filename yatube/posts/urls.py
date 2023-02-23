from django.urls import path, re_path

from . import views

app_name = 'posts'

urlpatterns = [
    path('follow/', views.FollowIndex.as_view(), name='follow_index'),
    path('profile/<str:username>/follow/',
         views.FollowView.as_view(), name='profile_follow'),
    path('profile/<str:username>/unfollow/',
         views.UnfollowView.as_view(), name='profile_unfollow'),
    path('posts/<pk>/commentapi/',
         views.CreateComment.as_view(), name='add_comment_api'),
    path('posts/<pk>/comment/',
         views.PostDetailWithCommentFormView.as_view(), name='add_comment'),
    path('postsapi/<pk>/', views.PostDetail.as_view(), name='postapi_detail'),
    path('posts/<pk>/',
         views.PostDetailWithCommentFormView.as_view(), name='post_detail'),
    path('get_groups_api/', views.GetGroups.as_view(), name='get_groups_api'),   
    path('creategalleryapi/', views.CreateGalleryPost.as_view(), name='create_gallery_api'),   
    path('create/', views.PostCreate.as_view(), name='post_create'),
    path('groupapi/<slug>/', views.GetGroupPostList.as_view(), name='groupapi_list'),
    path('group/<str:slug>/', views.GroupPosts.as_view(), name='group_list'),
    path('profileapi/<username>/', views.GetSingleAuthorPosts.as_view(), name='profileapi'),
    path('profile/<str:username>/', views.Profile.as_view(), name='profile'),
    path('posts/<pk>/edit/', views.PostEdit.as_view(), name='post_edit'),
    re_path(r'^postsapi$', views.GetPostsList.as_view(), name='postsapi'),
    path('indexapi/', views.IndexApi.as_view(), name='index_api'),
    path('', views.IndexView.as_view(), name='index'),
    path('galleryapi/', views.GalleryView.as_view(), name='gallery_api'),
    path('imageapi/', views.ImageView.as_view(), name='image_api'),
    path('getcurrentuser/', views.GetCurrentUsername.as_view(), name='getcurrentuser'),
    path('deletepost/<pk>', views.DeletePost.as_view(), name='deletepost'),
]
