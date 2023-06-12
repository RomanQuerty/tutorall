from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index_page, name='index'),
    path('find', views.find_page, name='find'),
    path('register', views.register_page, name='register'),
    path('sign', views.sign_page, name='sign'),
    path('become', views.become_page, name='become'),
    path('table', views.table_page, name='table'),
    path('profile', views.profile_page, name='profile'),
    path('quit', views.logout_page, name='logout'),
    path('save_table', views.save_table_view, name='save_table'),
    path('faq', views.faq_page, name='faq'),
    path('teacher/<int:teacher_id>', views.selected_profile_page, name='selected_teacher'),
    path('table/<int:teacher_id>', views.table_stud_page, name='table_stud_page'),
    path('upload', views.image_upload_view, name='upload'),
    path('submit-comment', views.submit_comment_view, name='submit_comment'),
]
