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
            User.objects.filter(id=pk).delete()
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
