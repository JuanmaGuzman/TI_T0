from django.urls import path

from . import views

urlpatterns = [
    # ex: /authyapp/user/
    path('reset', views.reset, name='reset'),
    # ex: /authyapp/user/
    path('users', views.user, name='user'),
    # ex: /authyapp/user/5/
    path('users/<int:user_id>', views.user_info, name='user_info'),
    # ex: /oauth/request/
    path('oauth/request', views.authorization_request, name='authorization_request'),
    # ex: /oauth/grant/
    path('oauth/grant', views.authorization_accepted, name='authorization_accepted'),
    # ex: /authyapp/user/5/
    path('users/<int:user_id>/basic', views.basic, name='basic'),
    # ex: /authyapp/user/5/
    path('users/<int:user_id>/work', views.work, name='work'),
    # ex: /authyapp/user/5/
    path('users/<int:user_id>/medical', views.medical, name='medical'),
    # ex: /authyapp/user/5/
    path('users/<int:user_id>/education', views.education, name='education'),
]