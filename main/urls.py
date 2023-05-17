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
    path('tableStud', views.tableStud_page, name='tableStud'),
    path('profile', views.profile_page, name='profile'),
    path('quit', views.logout_page, name='logout'),
    path('save_table', views.save_table_view, name='save_table'),
]
