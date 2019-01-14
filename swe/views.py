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
        uid = request.POST.get('uid')
        password = request.POST.get('password')
        user = authenticate(userid=uid, password=password)

        if user is not None:
            auth_login(request, user)
            return render(request, 'index.html', {})
        else:
            return render(request, 'login.html', {})

    else:
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, 'login.html', {})

# response of: example.com/logout/			
@login_required(login_url='/login/')
def logout(request):
    """
    if the requested user is not already logged in then render to login page
    else logout the user and render the logout page
    """
    auth_logout(request)
    return render(request, 'logout.html', {})

# response of: example.com/batch/	
def batchlist(request):
    """
    retrieve all the rows from `batch` table and make a dictionary
    and render the template with that dictionary
    """
    queryset = Batch.objects.all()
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
@login_required(login_url='/login/')
def profile(request, user_id):
    """
    if the request user is not authenticated the return to login page
    else:
        POST request:

        GET request:

        TODO:
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


    # load the information
    # student id
    if(len(user_id) == 10):
        try:
            s = Student.objects.get(regid=user_id)
            context = {'user' : s }
            return render(request, 'profile.html', context)

        except ObjectDoesNotExist as e:
            return render(request, 'error404.html',{})

    # teacher id
    elif(len(user_id) == 8):
        try:
            t = Teacher.objects.get(hid=user_id)
            context = {'user' : t }
            return  render(request, 'profile.html', context)
        except ObjectDoesNotExist as e:
            return render(request, 'error404.html',{})

    return render(request, 'error404.html',{})

# response of: example.com/feeds/
def feeds(request):
    return render(request, 'feeds.html', {})

# custom error request response
def error404(request):
    context = {}
    return render(request, 'error404.html', context)
