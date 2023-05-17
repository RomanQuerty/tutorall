import dataclasses
from typing import Any

from django.contrib.auth import authenticate, login, logout
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
    if request.user.is_authenticated:
        return {
            'header_elements': [
                HeaderElement(href="/", text='Главная'),
                HeaderElement(href="find", text='Поиск репетитора'),
                HeaderElement(href="profile", text='Профиль'),
                HeaderElement(href="quit", text='Выход'),
            ]
        }

    return {
        'header_elements': [
            HeaderElement(href="/", text='Главная'),
            HeaderElement(href="find", text='Поиск репетитора'),
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


def profile_page(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main:sign'))

    context = get_context(request)

    user_type_map = {
        AppUser.TEACHER: 'учителя',
        AppUser.STUDENT: 'ученика',
    }

    context.update({
        'user_first_name': request.user.first_name,
        'description': request.user.app_user.description,
        'user_type': user_type_map[request.user.app_user.user_type],
    })

    return render(request, 'main/profile.html', context)


def table_page(request: HttpRequest) -> HttpResponse:
    context = get_context(request)
    return render(request, 'main/table.html', context)


def tableStud_page(request: HttpRequest) -> HttpResponse:
    context = get_context(request)
    return render(request, 'main/tableStud.html', context)


def logout_page(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponseRedirect(reverse('main:sign'))
