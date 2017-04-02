from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from management.models import MyUser, Task, TaskFile
from django.core.urlresolvers import reverse
from crawler.get_bs4 import crawler
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
                    if file_have_list == []:
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


def view_task_data(request):
    if request.method == 'POST':
        id = request.POST.get('task_id', '')
        index = request.POST.get('data_id', '')
        task = Task.objects.get(id=id)
        file_list = TaskFile.objects.filter(task=task)
        data_detail = []
        file_name = file_list[int(index)].name
        '''
        file_path = os.path.join(STATIC_ROOT, "data\\").replace('\\', '/')
        csvfile = open(file_path + 'id' + file_name, 'r')
        reader = csv.reader(csvfile)
        for line in reader:
            data_detail.append(line)
        '''

        content = {
            'task': task,
            'data_list': file_list,
            'active_menu': 'view_data',
            'data_detail': json.dumps(data_detail),
        }
        return render(request, 'management/view_task_data.html', content)
