import dataclasses
import json
from typing import Any

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse

from main.models import AppUser, ScheduleTableCell
from main.table_generator import generate_table


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
            HeaderElement(href="sign", text='Вход'),
            HeaderElement(href="register", text='Регистрация'),
        ]
    }


@dataclasses.dataclass
class Teacher:
    name: str
    subject: str
    location: str


def get_teachers(request: HttpRequest) -> list[Teacher]:
    user_teachers = User.objects.filter(
        app_user__user_type=AppUser.TEACHER,
    )

    if request.GET.get('subject'):
        user_teachers = user_teachers.filter(
            app_user__subject__contains=request.GET.get('subject')
        )

    if request.GET.get('location'):
        user_teachers = user_teachers.filter(
            app_user__location__contains=request.GET.get('location')
        )

    if request.GET.get('name'):
        user_teachers = user_teachers.filter(
            first_name__contains=request.GET.get('name')
        )

    return [
        Teacher(
            name=user.first_name,
            subject=user.app_user.subject,
            location=user.app_user.location,
        )
        for user in user_teachers
    ]


def find_page(request: HttpRequest) -> HttpResponse:
    context = get_context(request)
    context.update({
        'teachers': get_teachers(request)
    })

    return render(request, 'main/find.html', context)


def register_page(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main:index'))

    if request.method == 'GET':
        context = get_context(request)
        return render(request, 'main/regist.html', context)

    user_type = AppUser.STUDENT
    if request.POST['userType'] == 'преподаватель':
        user_type = AppUser.TEACHER

    django_user = User.objects.create_user(
        first_name=request.POST['name'],
        username=request.POST['email'],
        email=request.POST['email'],
        password=request.POST['password'],
    )

    AppUser.objects.create(
        django_user_ref=django_user,
        user_type=user_type
    )

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
    if request.user.is_authenticated:
        context.update({
            'href': '/table',
            'main_text': 'Смотреть расписание',
            'additional_text': 'Смотреть расписание',
        })
    else:
        context.update({
            'href': '/register',
            'main_text': 'Зарегистрироваться',
            'additional_text': 'Зарегистрироваться',
        })

    return render(request, 'main/main.html', context)


@dataclasses.dataclass
class ProfileSetting:
    id: str
    value: str
    label_text: str


def get_profile_setting(user: User) -> list[ProfileSetting]:
    settings = [
        ProfileSetting(
            id='name',
            value=user.first_name,
            label_text='Имя',
        ),
        ProfileSetting(
            id='description',
            value=user.app_user.description,
            label_text='Описание',
        )
    ]
    if user.app_user.user_type == AppUser.STUDENT:
        return settings

    settings.extend([
        ProfileSetting(
            id='location',
            value=user.app_user.location,
            label_text='Местоположение',
        ),
        ProfileSetting(
            id='subject',
            value=user.app_user.subject,
            label_text='Предмет',
        ),
    ])

    return settings


def save_profile(request: HttpRequest) -> HttpResponse:
    user = request.user
    app_user = user.app_user

    user.first_name = request.POST['name']
    app_user.description = request.POST['description']

    if app_user.user_type == AppUser.TEACHER:
        app_user.location = request.POST['location']
        app_user.subject = request.POST['subject']

    user.save()
    app_user.save()


def profile_page(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main:sign'))

    if request.method == 'POST':
        save_profile(request)
        return HttpResponse('success')

    context = get_context(request)

    user_type_map = {
        AppUser.TEACHER: 'учителя',
        AppUser.STUDENT: 'ученика',
    }

    context.update({
        'user_first_name': request.user.first_name,
        'description': request.user.app_user.description,
        'user_type': user_type_map[request.user.app_user.user_type],
        'profile_settings': get_profile_setting(request.user),
    })

    return render(request, 'main/profile.html', context)


def table_page(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main:sign'))

    context = get_context(request)
    context.update({
        'time_and_cells_list': generate_table(request.user.app_user),
    })

    return render(request, 'main/table.html', context)


def save_table_view(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponse(
            'This endpoint accept only posts',
            status=400,
        )

    request_body_json = json.loads(request.body.decode("utf-8"))

    active_cells = request_body_json['active']

    ScheduleTableCell.objects.filter(
        teacher=request.user.app_user
    ).delete()

    for cell in active_cells:
        row_number = cell['row']
        week_day = cell['col']

        ScheduleTableCell.objects.create(
            teacher=request.user.app_user,
            week_day=week_day,
            row_number=row_number,
        )

    return HttpResponse('success', 200)


def tableStud_page(request: HttpRequest) -> HttpResponse:
    context = get_context(request)
    return render(request, 'main/tableStud.html', context)


def logout_page(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponseRedirect(reverse('main:sign'))


def faq_page(request: HttpRequest) -> HttpResponse:
    context = get_context(request)
    return render(request, 'main/faq.html', context)
