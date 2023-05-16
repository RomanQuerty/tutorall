from django.shortcuts import render
from django.http import HttpRequest


# Create your views here.

def find_page(request: HttpRequest):
    return render(request, 'main/find.html')


def register_page(request: HttpRequest):
    return render(request, 'main/regist.html')


def sign_page(request: HttpRequest):
    return render(request, 'main/sign.html')


def become_page(request: HttpRequest):
    return render(request, 'main/become.html')


def index_page(request: HttpRequest):
    return render(request, 'main/main.html')
