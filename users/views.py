from users.models import Statuses, Tasks, Labels
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import gettext as _
from .forms import UserForm


MAIN = 'base.html'
LOGIN = '/login/'
LOGOUT = '/logout/'
USERS = 'users/users.html'
CREATE = 'registration/create.html'
DELETE = 'users/delete.html'
STATUS_READ = 'statuses/status_read.html'
STATUS_CREATE = 'statuses/status_create.html'
STATUS_UPDATE = 'statuses/status_update.html'
STATUS_DELETE = 'statuses/status_delete.html'
TASK_READ = 'tasks/task_read.html'
TASK_CREATE = 'tasks/task_create.html'
TASK_UPDATE = 'tasks/task_update.html'
TASK_DELETE = 'tasks/task_delete.html'
TASK_VIEW = 'tasks/task_view.html'
LABEL_READ = 'labels/label_read.html'
LABEL_CREATE = 'labels/label_create.html'
LABEL_UPDATE = 'labels/label_update.html'
LABEL_DELETE = 'labels/label_delete.html'

# users


def base(request):
    return render(request, MAIN, {})


def logged_in_message(sender, user, request, **kwargs):
    messages.success(request, _('You are logged in'))


def logged_out_message(sender, user, request, **kwargs):
    messages.info(request, _('You are logged out'))


def logged_failed_message(sender, request, **kwargs):
    messages.error(request, _('Please enter the correct username and password. Both fields can be case sensitive.'))


user_logged_in.connect(logged_in_message)
user_logged_out.connect(logged_out_message)
user_login_failed.connect(logged_failed_message)


def users(request):
    user_list = User.objects.all()
    page = request.GET.get('page', 1)
    user_list.all
    paginator = Paginator(user_list, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, USERS, {'users': users})


def create(request, msg=True):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            if msg:
                messages.success(request, _('User registered successfully'))
            return redirect(LOGIN)

    else:
        form = UserForm()

    return render(request, CREATE, {'form': form})


def delete(request, pk=0, msg=True):
    if request.user.is_authenticated and pk == request.user.id:
        if request.method == 'POST':
            try:
                User.objects.filter(id=pk).delete()
            except Exception as e:
                messages.error(request, _('There is a task on user'))
                msg = False
            if msg:
                messages.success(request, _('User deleted successfully'))
            return redirect('/users/')

        return render(request, DELETE)
    else:
        if not request.user.is_authenticated:
            messages.error(request, _('You are not login! Please, login'))
        elif request.user.id != pk:
            messages.error(request, _('You do not have permission for another user change'))
            return redirect('/users/')

        return redirect(LOGIN)


def update(request, pk=0):
    if request.user.is_authenticated and pk == request.user.id:
        form = UserForm(request.POST)
        if request.method == 'POST' and (form.is_valid() or request.POST['username'] == request.user.username):
            delete(request, pk, msg=False)
            create(request, msg=False)
            messages.success(request, _('User updated successfully'))
            return redirect('/users/')

        return create(request)
    else:
        return delete(request, pk)


def check_logged_user(fun):
    def wrapper(request, pk=0):
        if not request.user.is_authenticated:
            return base(request)
        else:
            if fun.__code__.co_argcount == 2:
                return fun(request, pk)
            return fun(request)
    return wrapper

# statuses


@check_logged_user
def statuses_read(request):
    return render(request, STATUS_READ, {'statuses': Statuses.objects.all()})


@check_logged_user
def statuses_create(request):
    if request.method == 'POST':
        Statuses(name=request.POST.get('name')).save()
        messages.success(request, _('Status created successfully'))
        return redirect('/statuses/')

    return render(request, STATUS_CREATE, {})


@check_logged_user
def statuses_delete(request, pk=0):
    if request.method == 'POST':
        Statuses.objects.filter(id=pk).delete()
        messages.success(request, _('Status delete successfully'))
        return redirect('/statuses/')

    name = Statuses.objects.filter(id=pk).all()[0]
    return render(request, STATUS_DELETE, {'name': name})


@check_logged_user
def statuses_update(request, pk=0):
    statuses = Statuses.objects.filter(id=pk)

    if request.method == 'POST':
        try:
            statuses.update(name=request.POST.get('name'))
        except Exception as e:
            fields = {'name': request.POST.get('name'), 'error': _('Name already exist')}
            return render(request, STATUS_UPDATE, fields)

        messages.success(request, _('Status updated successfully'))
        return redirect('/statuses/')

    return render(request, STATUS_UPDATE, {'name': statuses.all()[0]})

# tasks


@check_logged_user
def tasks_read(request):
    return render(request, TASK_READ, {'tasks': Tasks.objects.all()})


@check_logged_user
def tasks_create(request):
    if request.method == 'POST':
        task = Tasks(
            name=request.POST.get('name'),
            autor=User.objects.get(id=request.user.id),
            description=request.POST.get('description'),
            status=Statuses.objects.get(id=request.POST.get('status')),
            user=User.objects.get(id=request.POST.get('executor')),
        )
        task.save()
        for label in request.POST.getlist('labels'):
            task.label.add(Labels.objects.get(id=label))

        messages.success(request, _('Task created successfully'))
        return redirect('/tasks/')

    return render(request, TASK_CREATE, {'labels': Labels.objects.all(), 'statuses': Statuses.objects.all(), 'users': User.objects.all()})


@check_logged_user
def tasks_delete(request, pk=0):
    if request.method == 'POST':
        Tasks.objects.filter(id=pk).delete()
        messages.success(request, _('Tasks delete successfully'))
        return redirect('/tasks/')

    user = str(User.objects.get(id=request.user.id))
    autor = str(Tasks.objects.get(id=pk).autor)

    if autor != user:
        messages.error(request, _('A task can only be deleted by its author'))
        return redirect('/tasks/')

    name = Tasks.objects.filter(id=pk).all()[0]
    return render(request, TASK_DELETE, {'name': name})


@check_logged_user
def tasks_update(request, pk=0):
    tasks = Tasks.objects.filter(id=pk)

    if request.method == 'POST':
        try:
            tasks.delete()
            task = Tasks(
                name=request.POST.get('name'),
                autor=User.objects.get(id=request.user.id),
                description=request.POST.get('description'),
                status=Statuses.objects.get(id=request.POST.get('status')),
                user=User.objects.get(id=request.POST.get('executor')),
            )
            task.save()
            for label in request.POST.getlist('labels'):
                task.label.add(Labels.objects.get(id=label))
          
        except Exception as e:
            print(e)
            fields = {
                'tasks': tasks,
                'statuses': Statuses.objects.all(),
                'users': User.objects.all(),
                'labels': Labels.objects.all(),
                'error': _('Name already exist'),
            }
            return render(request, TASK_UPDATE, fields)

        messages.success(request, _('Task updated successfully'))
        return redirect('/tasks/')

    tables = {
        'tasks': tasks,
        'statuses': Statuses.objects.all(),
        'users': User.objects.all(),
        'labels': Labels.objects.all(),
    }

    return render(request, TASK_UPDATE, tables)


@check_logged_user
def tasks_view(request, pk=0):
    return render(request, TASK_VIEW, {'tasks': Tasks.objects.filter(id=pk)})


# labels


@check_logged_user
def labels_read(request):
    return render(request, LABEL_READ, {'labels': Labels.objects.all()})


@check_logged_user
def labels_create(request):
    if request.method == 'POST':
        Labels(name=request.POST.get('name')).save()
        messages.success(request, _('Label created successfully'))
        return redirect('/labels/')

    return render(request, LABEL_CREATE, {})


@check_logged_user
def labels_delete(request, pk=0):
    if request.method == 'POST':
        Labels.objects.filter(id=pk).delete()
        messages.success(request, _('Label delete successfully'))
        return redirect('/labels/')

    if len(Tasks.objects.filter(label__in=[pk]).distinct()) > 0:
        messages.error(request, _('Label have task(s)'))
        return redirect('/labels/')

    name = Labels.objects.filter(id=pk).all()[0]
    return render(request, LABEL_DELETE, {'name': name})


@check_logged_user
def labels_update(request, pk=0):
    labels = Labels.objects.filter(id=pk)

    if request.method == 'POST':
        try:
            labels.update(name=request.POST.get('name'))
        except Exception as e:
            fields = {'name': request.POST.get('name'), 'error': _('Name already exist')}
            return render(request, LABEL_UPDATE, fields)

        messages.success(request, _('Label updated successfully'))
        return redirect('/labels/')

    return render(request, LABEL_UPDATE, {'name': labels.all()[0]})
