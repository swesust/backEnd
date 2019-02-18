from django.contrib.auth.decorators import login_required
from django.contrib.auth import ( authenticate,
    login as auth_login, logout as auth_logout)
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect, HttpResponse
from django.template import loader

from swe.forms import (LoginForm, UserRecognize, ChangePasswordForm,
    UserToken)
from swe.helper import Token
from swe.models import AuthUser
from swe import variables as var


# response of: example.com/login/
def login(request):
    """
    POST request:
        retrieve the user id and password that inserted in the login form
        try to authenticate with this information. If the authentication
        method will return an object of AuthModel after successfully
        authentication. 

        Check the return value:
            if `None` that means login user is not valid so return to login page
            else call the `login` method to logged the user and return to home page


    GET request:
        if the requested user is already logged in or authenticated then return to home
        else render the login page 
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            uid = form.cleaned_data['userid']
            password = form.cleaned_data['password']
            user = authenticate(userid=uid, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('/')

            else:
                messages.error(request, "ID and Password didn't matched")

        else:
            messages.warning(request, 'Data is not valid')  
    else:
        if request.user.is_authenticated:
            return redirect('/')

    form = LoginForm()
    context = {
        'form' : form,
    }
    return render(request, var.LOGIN_TEMPLATE, context)

# response of: example.com/logout/			
@login_required(login_url=var.LOGIN_URL)
def logout(request):
    """
    if the requested user is not already logged in then render to login page
    else logout the user and render the logout page
    """
    auth_logout(request)
    return render(request, var.LOGOUT_TEMPLATE, {})


@login_required(login_url=var.LOGIN_URL)
def change_password(request):

    context = {
        'error' : False,
        'message' : ''
    }

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            if new_password != confirm_password:
                context['error'] = True
                context['message'] = 'New and Confirm Password not matched'

            else:
                user = authenticate(userid = request.user.userid, password = current_password)
                if user is not None:
                    # valid user
                    user.set_password(new_password)
                    user.save()

                    user = authenticate(userid = user.userid, password = new_password)
                    auth_login(request, user)

                    return HttpResponse('Passwod Changed Successfully')

                else:
                    context['error'] = True
                    context['message'] = 'Passwod not matched with user'
        else:
            context['error'] = True
            context['message'] = 'Invalid data'

    form = ChangePasswordForm()
    context['form'] = form

    return render(request, 'auth/change_password.html', context)


def forget_password(request):
    if request.method == 'POST':
        form = UserRecognize(request.POST)

        if  form.is_valid():
            try:
                userid = form.cleaned_data.get('userid')
                user = AuthUser.objects.get(userid = userid)
                token = Token.get_token(user.userid, user.password)
                # mail this
                send_mail(var.EMAIL_SUBJECT_TOKEN,
                    'Hello '+user.name+' '+var.EMAIL_TEXT_TOKEN+token,
                    var.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False)

                return redirect('/forget-password/varification')

            except Exception as e:
                context = {
                    'form' : form,
                    'invalid' : True}
                return render(request, 'auth/forget_password.html', context)
        else:
            context = {
                'form' : form,
                'invalid' : True}
            return render(request, 'auth/forget_password.html', context)

    form = UserRecognize()
    context = {
        'form' : form,
        'invalid' : False
    }    
    return render(request, 'auth/forget_password.html',context)


def forget_password_varification(request):

    if request.method == 'POST':
        form = UserToken(request.POST)

        if form.is_valid():
            token = form.cleaned_data.get('token')
            if Token.is_valid(token):
                # reset the password
                try:
                    # generate a new password
                    user_id = Token.get_userid(token)
                    user = AuthUser.objects.get(userid = user_id)

                    new_password = helper.new_password_request()
                    send_mail(var.EMAIL_SUBJECT_PASSWORD_RESET,
                         'Hello '+user.name+' '+var.EMAIL_TEXT_PASSWORD_RESET+new_password,
                        var.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False)

                    user.set_password(new_password)
                    user.save()
                    response = loader.get_template('auth/password_reset_done.html')
                    return HttpResponse(response.render({}, request))
                except Exception as e:
                    context = {
                        'form' : form,
                        'invalid' : True}
                    return render(request, 'auth/forget_password_varification.html', context)
       

        context = {
            'form' : form,
            'invalid' : True}
        return render(request, 'auth/forget_password_varification.html', context)
        
    form = UserToken()
    context = {
        'form' : form,
        'invalid' : False
    }
    return render(request, 'auth/forget_password_varification.html',context)

