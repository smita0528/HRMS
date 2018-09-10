from django.shortcuts import render, redirect
from . import models
from django import forms
from . import forms

import hashlib


def hash_code(s, salt='HRMS'):
    h = hashlib.sha3_256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def index(request):
    pass
    return render(request, 'login/index.html')


def login(request):
    # No duplicate enter
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = 'Please enter correct information!'

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            try:
                user = models.User.objects.get(name=username)

                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = 'password invalid!'
            except:
                message = "user doesn't exit!"

        return render(request, 'login/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "Please validate the information！"
        if register_form.is_valid():  # get data
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # to make sure both password are correct
                message = "both passwords are not match"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # check is username unique
                    message = 'please choose different username!'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # check unique email
                    message = 'this email has been used, please try again!'
                    return render(request, 'login/register.html', locals())

                # if everything is ok, then register

                new_user = models.User()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')  # auto jump to login page
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # if no log-in, then no log out
        return redirect('/index/')
    # class all the content in session in one time
    request.session.flush()

    return redirect('/index/')
