from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from main.models import AppUser


# Create your views here.

def find_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'main/find.html')


def register_page(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return render(request, 'main/regist.html')

    django_user = User.objects.create_user(
        username=request.POST['name'],
        email=request.POST['email'],
        password=request.POST['password'],
    )

    AppUser.objects.create(django_user_ref=django_user)

    return HttpResponse('success')


def sign_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'main/sign.html')


def become_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'main/become.html')


def index_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'main/main.html')


def student_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'main/student.html')


def teacher_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'main/teacher.html')

def table_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'main/table.html')

def tableStud_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'main/tableStud.html')