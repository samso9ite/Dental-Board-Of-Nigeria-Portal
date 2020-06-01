from django.urls import path
from . import views

app_name = 'profPortal'

urlpatterns = [
    path('dashboard/', views.Profile.as_view(), name='dashboard'),
    path('update/', views.Update.as_view(), name='update'),
    path('create_account/', views.ProfAccntView.as_view(), name='createAccount'),
    path('update_account/<int:pk>', views.ProfAccntUpdateView.as_view(), name='accountUpdate'),
] 