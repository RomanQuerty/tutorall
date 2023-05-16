from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index_page, name='index'),
    path('find', views.find_page, name='find'),
    path('register', views.register_page, name='register'),
    path('sign', views.sign_page, name='sign'),
    path('become', views.become_page, name='become'),
    path('teacher', views.teacher_page, name='teacher'),
    path('student', views.student_page, name='student'),
]
