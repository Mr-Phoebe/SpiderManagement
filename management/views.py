from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from management.models import MyUser, Task, TaskFile
from django.core.urlresolvers import reverse
from crawler.get_bs4 import crawler
from crawler.douban import crawle_douban
from crawler.get_function import *
from SP.settings import STATIC_ROOT
import csv

def index(request):
    user = request.user if request.user.is_authenticated() else None
    content = {
        'active_menu': 'homepage',
        'user': user,
    }
    return render(request, 'management/index.html', content)


def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if password == '' or repeat_password == '':
            state = 'empty'
        elif password != repeat_password:
            state = 'repeat_error'
        else:
            username = request.POST.get('username', '')
            if User.objects.filter(username=username):
                state = 'user_exist'
            else:
                new_user = User.objects.create_user(username=username, password=password,
                                                    email=request.POST.get('email', ''))
                new_user.save()
                new_my_user = MyUser(user=new_user, nickname=request.POST.get('nickname', ''))
                new_my_user.save()
                state = 'success'
    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None,
    }
    return render(request, 'management/signup.html', content)


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if not user.is_superuser:
                return HttpResponseRedirect(reverse('homepage'))
            else:
                return HttpResponseRedirect(('/admin'))
        else:
            state = 'not_exist_or_password_error'
    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None
    }
    return render(request, 'management/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('homepage'))


@login_required
def set_password(request):
    user = request.user
    state = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if user.check_password(old_password):
            if not new_password:
                state = 'empty'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                state = 'success'
        else:
            state = 'password_error'
    content = {
        'user': user,
        'active_menu': 'homepage',
        'state': state,
    }
    return render(request, 'management/set_password.html', content)


@login_required
def add_task(request):
    user = request.user
    state = None
    if request.method == 'POST':
        new_task = Task(
            name=request.POST.get('name', ''),
            user=user.myuser,
            url=request.POST.get('url', ''),
            content=request.POST.get('content', ''),
            hasfile=False
        )
        new_task.save()
        state = 'success'
    content = {
        'user': user,
        'active_menu': 'add_task',
        'state': state,
    }
    return render(request, 'management/add_task.html', content)

@login_required
def view_task_list(request):
    user = request.user
    task_list = Task.objects.filter(user=user.myuser)
    paginator = Paginator(task_list, 5)
    page = request.GET.get('page')
    try:
        task_list = paginator.page(page)
    except PageNotAnInteger:
        task_list = paginator.page(1)
    except EmptyPage:
        task_list = paginator.page(paginator.num_pages)
    content = {
        'user': user,
        'active_menu': 'view_task',
        'task_list': task_list,
    }
    return render(request, 'management/view_task_list.html', content)


@login_required
def task_detail(request):
    user = request.user
    task_id = request.GET.get('id', '')
    if task_id == '':
        return HttpResponseRedirect(reverse('view_task_list'))
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return HttpResponseRedirect(reverse('view_task_list'))
    content = {
        'user': user,
        'active_menu': 'view_task',
        'task': task,
    }
    return render(request, 'management/task_detail.html', content)


def view_douban(request):
    return render(request, 'management/douban.html')


@login_required
def douban(request):
    if request.method == 'POST':
        method = request.POST.get('task_method', '')
        crawle_douban(method)
        return JsonResponse({'code': 0})
    return JsonResponse({'code': 1})

@login_required
def crawl(request):
    if request.method == 'POST':
        id = request.POST.get('task_id', '')
        url = request.POST.get('task_url', '')
        content = request.POST.get('task_content', '')
        method = request.POST.get('task_method', '')
        try:
            file_list = crawler(id=id, url=url, string=content, method=method)
            if file_list != []:
                task = Task.objects.get(id=id)
                task.hasfile = True
                task.method = True if method == 'true' else False
                task.save()
                for file_name in file_list:
                    file_have_list = TaskFile.objects.filter(name=file_name, task=task)
                    if len(file_have_list) == 0:
                        new_file = TaskFile(
                            name=file_name,
                            task=task
                        )
                        new_file.save()
                return JsonResponse({'code': 0})
            else:
                return JsonResponse({'code': -1, 'msg': '没有抓取内容'})
        except Exception as e:
            return JsonResponse({'code': -1, 'msg': e})
    return JsonResponse({'code': 1})


def download(request):
    file_path = os.path.join(STATIC_ROOT, "data\\").replace('\\', '/')
    if request.method == 'POST':
        id = request.POST.get('task_id', '')
        zip_name = make_zip(file_path, id)
        return JsonResponse({'code': 0, 'url': '/static/data/' + zip_name})
    return JsonResponse({'code': 1})


def download_douban(request):
    file_path = os.path.join(STATIC_ROOT, "data\\").replace('\\', '/')
    if request.method == 'POST':
        zip_name = make_zip(file_path, '0')
        return JsonResponse({'code': 0, 'url': '/static/data/' + zip_name})
    return JsonResponse({'code': 1})

def view_task_data(request):
    user = request.user
    id = request.GET.get('task_id', '')
    index = request.GET.get('data_id', '')
    task = Task.objects.get(id=id)
    file_list = TaskFile.objects.filter(task=task)
    data_detail = []
    file_name_list = []
    num = 0
    for taskfile in file_list:
        file_name_list.append((num, taskfile.name))
        num += 1
    if len(file_name_list) == 0:
        content = {
            'user': user,
            'active_menu': 'view_task',
            'task': task,
        }
        return render(request, 'management/task_detail.html', content)
    else:
        file_name = file_list[int(index)].name

        file_path = os.path.join(STATIC_ROOT, "data\\").replace('\\', '/')
        csvfile = open(file_path + id + '/' + file_name, 'r', encoding='utf-8')
        reader = csv.reader(csvfile)
        num = 1
        for line in reader:
            line = [num] + line
            num += 1
            data_detail.append(line)
        paginator = Paginator(data_detail, 25)
        page = request.GET.get('page')
        try:
            data_detail = paginator.page(page)
        except PageNotAnInteger:
            data_detail = paginator.page(1)
        except EmptyPage:
            data_detail = paginator.page(paginator.num_pages)

        content = {
            'task': task,
            'data_id': index,
            'file_name_list': file_name_list,
            'active_menu': 'view_data',
            'data_detail': data_detail,
        }
        return render(request, 'management/view_task_data.html', content)
