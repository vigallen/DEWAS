from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseNotAllowed, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader, Context
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from YAAS.forms import UserCreationForm, ChangeEmail


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


'''def edituser(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserChangeForm()
    return render(request, 'edituser.html', {'form': form})
'''


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your Password was updated!')
            return redirect('home')
        else:
            messages.error(request, 'There was an error with your submission, please correct it.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


def home(request):
    return render(request, 'home.html')
# Create your views here.


@login_required
def change_email(request):
    user = User.objects.get(pk=request.user.pk)
    if request.method == 'POST':
        form = ChangeEmail(request.POST)
        if form.is_valid():
            if form.cleaned_data['email'] == form.cleaned_data['email_confirm']:
                user.email = form.cleaned_data['email']
                user.save()
                return HttpResponseRedirect('/')
            else:
                form = ChangeEmail(request.POST)
    else:
        form = ChangeEmail(request.POST)
    return render(request, 'email.html', {'form': form})
