from django.urls import path, re_path
from django.conf.urls import url, include
from . import views
from django.contrib.auth.urls import views as auth_views

app_name = 'Auth'

urlpatterns = [
    path('sign_up', views.sign_up_view, name='Register'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(),
        name='password_reset'),
    url(r'^password_reset/done/$',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
    path('logout/', views.logout_view, name="logout"),
    path('resetPassword/', views.change_password_view, name="sch_pwd_reset"),
    path('adminPasswordReset/', views.change_password_view, name="adminPasswordReset"),
   ]


