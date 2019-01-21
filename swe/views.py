from django.shortcuts import render
from swe.models import *
from . import helper
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.core.files.uploadedfile import UploadedFile, TemporaryUploadedFile
from PIL import Image as ImageProcess
from io import BytesIO
from swe.helper import Image
from django.core.files.storage import FileSystemStorage as FSS
from django.contrib.auth import (
	authenticate, logout as auth_logout, login as auth_login)
from django.contrib.auth.decorators import login_required
from . import variables as var
from swe.forms import LoginForm, UserRecognize, UserToken
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template import loader

# Create your views here.

# response of: example.com/
def index(request):
    return render(request, 'index.html', {})

# response of: example.com/faculty/
def faculty(request):
    # retrive all rows from `teachers` table
    teachers = Teacher.objects.all()
    # set the dictionary
    context = {'teachers' : teachers }
    # render the template with this dictionary
    return render(request, 'faculty.html', context)

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
                return render(request, var.INDEX_TEMPLATE, {})

            else:
                context = {
                    'form' : form,
                    'invalid' : True
                }
                return render(request, var.LOGIN_TEMPLATE, context)

        else:
            context = {
                'form' : form,
                'invalid' : True
            }
            return render(request, var.LOGIN_TEMPLATE, context)            

    else:
        if request.user.is_authenticated:
            return redirect('/')
        else:
            form = LoginForm()
            context = {
                'form' : form,
                'invalid' : False
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

# response of: example.com/batch/	
def batchlist(request):
    """
    retrieve all the rows from `batch` table and make a dictionary
    and render the template with that dictionary
    """
    queryset = Batch.objects.all()[::-1]
    context = {
        'queryset' : queryset,
    }
    return render(request, 'batchlist.html', context)

# response of: example.com/batch/year/
def batch(request, batch_id):
    """
    check the batch year is valid or not.
    if valid then filter all the students of this batch then render the template
    with the batch and students data dictionary.
    """
    try:
        batch = Batch.objects.get(year=batch_id)
        students = Student.objects.filter(batch=batch).order_by('regid')
        context = {
            'batch' : batch, 
            'students' : students}
        return render(request, 'batch.html', context)

    except ObjectDoesNotExist as e:
        return render(request, 'error404.html', {})

# response of: example.com/userid
def profile(request, user_id):
    """
    POST Request:
    """
    if request.method == 'POST':
        data = request.FILES
        imgsrc = data.get('profile')
        if imgsrc != None:

            # from name check the file format : jpg, jpeg, .png
            if Image.isValidFormat(imgsrc.name):
                if imgsrc.multiple_chunks(2500000):
                    imgsrc.chunks(2500000)
                # read the stream
                bytedata = imgsrc.read()

                # for students
                if len(user_id) == 10:
                    user = Student.objects.get(regid=user_id)
                    Image.save(user, bytedata)
                elif len(user_id) == 8:
                    user = Teacher.objects.get(hid=user_id)
                    Image.save(user, bytedata)

    """
    try to fetch the requested user account. If the account exist then
    check the account type; whether its a student account or teacher account
    and then fetch the profile from the particular model
    """
    try:
        user = AuthUser.objects.get(userid = user_id)
        profile = None
        if user.is_student:
            profile = Student.objects.get(user = user)
        else:
            profile = Teacher.objects.get(user = user)

        """
        set up the context:
            1. whether the requested user is an authenticated user
            2. whether the user is trying to access self account
        """

        is_auth = request.user.is_authenticated
        is_self = False
        if is_auth:
            # checking the request user is trying to access his/her/ze's account
            is_self = (request.user.userid == user_id)

        context = {
            'user' : user,
            'profile' : profile,
            'is_auth' : is_auth,
            'is_self' : is_self
        }
        if user.is_student:
            return render(request, 'profiles/student.html', context)
        else:
            return render(request, 'profiles/teacher.html', context)

    except ObjectDoesNotExist as e:
        return HttpResponse('User Profile Not Found') 


# response of: example.com/feeds/
def feeds(request):
    posts = Post.objects.order_by('time', 'date')[::-1]
    context = {
        'posts' : posts
        }
    return render(request, 'feeds.html', context)


def feed_delete(request, pk):
    try:
        Post.objects.get(pk = pk).delete()
        # redirect to current page
        return redirect('/feeds')
    except ObjectDoesNotExist as e:
        return HttpResponse("Post not found")
# custom error request response
def error404(request):
    context = {}
    return render(request, 'error404.html', context)


def forget_password(request):
    if request.method == 'POST':
        form = UserRecognize(request.POST)

        if  form.is_valid():
            try:
                userid = form.cleaned_data.get('userid')
                user = AuthUser.objects.get(userid = userid)
                token = helper.Token.get_token(user.userid, user.password)
                # mail this
                send_mail('Password Reset Token',
                    'Your token: '+token,
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
            if helper.Token.is_valid(token):
                # reset the password
                try:
                    # generate a new password
                    user_id = helper.Token.get_userid(token)
                    user = AuthUser.objects.get(userid = user_id)

                    send_mail('New Password',
                        'pass12345',
                        var.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False)

                    user.set_password('pass12345')
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

