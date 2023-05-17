import dataclasses
from typing import Any

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse

from main.models import AppUser


# Create your views here.


@dataclasses.dataclass
class HeaderElement:
    href: str
    text: str


def get_context(request: HttpRequest) -> dict[str, Any]:
    return {
        'header_elements': [
            HeaderElement(href="/", text='Главная'),
            HeaderElement(href="find", text='Найти репетитора'),
            HeaderElement(href="become", text='Стать репетитором'),
            HeaderElement(href="sign", text='Вход'),
        ]
    }


def find_page(request: HttpRequest) -> HttpResponse:
    context = get_context(request)
    return render(request, 'main/find.html', context)


def register_page(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main:index'))

    if request.method == 'GET':
        context = get_context(request)
        return render(request, 'main/regist.html', context)

    django_user = User.objects.create_user(
        first_name=request.POST['name'],
        username=request.POST['email'],
        email=request.POST['email'],
        password=request.POST['password'],
    )

    AppUser.objects.create(django_user_ref=django_user)

    return HttpResponse('success')


def sign_page(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main:index'))

    if request.method == 'GET':
        context = get_context(request)

        return render(request, 'main/sign.html', context)

    username = str(request.POST['email'])
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)

    if not user:
        return HttpResponse('Wrong login or password', status=401)

    login(request, user)
    return HttpResponse('success')


def become_page(request: HttpRequest) -> HttpResponse:
    context = get_context(request)
    return render(request, 'main/become.html', context)


def index_page(request: HttpRequest) -> HttpResponse:
    context = get_context(request)
    return render(request, 'main/main.html', context)


def student_page(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main:sign'))

    context = get_context(request)
    context.update({
        'user_first_name': request.user.first_name,
        'description': request.user.app_user.description,
    })

    return render(request, 'main/student.html', context)


def teacher_page(request: HttpRequest) -> HttpResponse:
    context = get_context(request)
    return render(request, 'main/teacher.html', context)


def table_page(request: HttpRequest) -> HttpResponse:
    context = get_context(request)
    return render(request, 'main/table.html', context)


def tableStud_page(request: HttpRequest) -> HttpResponse:
    context = get_context(request)
    return render(request, 'main/tableStud.html', context)
