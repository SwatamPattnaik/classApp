from django.urls import path
from . import views

app_name = 'class_details'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('user_registration/', views.user_registration, name='user_registration'),
    path('admin/', views.admin, name='admin'),
    path('update_status/', views.update_status, name='update_status'),
    path('add_class/', views.add_class, name='add_class'),
    path('student_form/<str:student_id>', views.student_form, name='student_form')
]