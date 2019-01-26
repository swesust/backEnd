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
from swe.forms import (
    LoginForm, UserRecognize, UserToken, EndrosementForm, WorkingForm)
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template import loader
from django.utils.timezone import datetime

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
                return redirect('/')

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
    POST request

    
        Working:
            Company Name = 'company'
            Position = 'jobPosition'
            From Date = 'startingDate'
            Is working = 'stillWorking'
            To Date = 'endingDate'
            Comment  = 'jobComment'


        Endrosements:
            #options



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

        # fetch all endrosements of this user
        endrosements = Endrosement.objects.filter(user=user)

        endrose_form = EndrosementForm()
        context = {
            'user' : user,
            'profile' : profile,
            'is_auth' : is_auth,
            'is_self' : is_self,
            'endrosements' : endrosements,
            'endrose_form' : endrose_form
        }
        if user.is_student:
            # fetch all working information of this user
            works = Working.objects.filter(user=user)
            context['works'] = works
            return render(request, 'profiles/student.html', context)
        else:
            return render(request, 'profiles/teacher.html', context)

    except ObjectDoesNotExist as e:
        return HttpResponse('User Profile Not Found') 


# response of: example.com/userid/edit
@login_required(login_url=var.LOGIN_URL)
def profile_edit(request, user_id):
    if request.user.userid != user_id:
        return redirect('/'+user_id+'/')


    """
    POST request:

    User and Profile:
        Profile Image = 'profilePic'
        Cover Image = 'coverPic'
        User Name = 'name'
        User Emal = 'email'
        Profile Phone = 'phone'
        Student Profile Address = 'address'
        Profile Alumni = 'alumni'


    Integrated Profile:
        Facebook = 'facebookid'
        Github = 'githubid'
        Twitter = 'twitterid'
        LinkedIn = 'linkedinid'

    """
    
    # profile edit

    if request.method == 'POST':
        data = request.POST
        password = data.get('password')
        user = authenticate(userid=request.user.userid, password = password)

        if user == None:
            return HttpResponse('Unknown password')

        elif user != request.user:
            return HttpResponse('Invalid User')

        if user.is_student:
            profile = Student.objects.get(user = user)
        else:
            profile = Teacher.objects.get(user = user)

        files = request.FILES

        profile_img = files.get('profile_img')
        cover_img = files.get('cover_img')

        if profile_img != None:
            if Image.is_valid_format(profile_img.name):
                if profile_img.multiple_chunks(var.FILE_CHUNK):
                    profile_img.chunks(var.FILE_CHUNK)

                bytes_data = profile_img.read()
                if user.is_student:
                    profile.imgsrc = Image.save(var.FOLDER_STUDENT, bytes_data)
                else:
                    profile.imgsrc = Image.save(var.FOLDER_TEACHER, bytes_data)


        if cover_img != None:
            if Image.is_valid_format(cover_img.name):
                if cover_img.multiple_chunks(var.FILE_CHUNK):
                    cover_img.chunks(var.FILE_CHUNK)

                bytes_data = cover_img.read()
                if user.is_student:
                    profile.cover = Image.save(var.FOLDER_STUDENT, bytes_data)
                else:
                    profile.cover = Image.save(var.FOLDER_TEACHER, bytes_data)


        user.name = data.get('name')
        user.email = data.get('email')
        profile.phone = data.get('phone')

        alumni = data.get('alumni')

        if alumni is not None:
            profile.alumni = True
        else:
            profile.alumni = False



        if user.is_student:
            profile.address = data.get('address')
            githubid = data.get('githubid')
            facebookid = data.get('facebookid')
            linkedinid = data.get('linkedinid')
            twitterid = data.get('twitterid')

            if githubid is not None:
                profile.githubid = githubid
            else:
                profile.githubid = 'home'
            if facebookid is not None:
                profile.facebookid = facebookid
            else:
                profile.facebookid = 'home'
            if linkedinid is not None:
                profile.linkedinid = linkedinid
            else:
                profile.linkedinid = 'home'
            if twitterid is not None:
                profile.twitterid = twitterid
            else:
                profile.twitterid = 'home'

        user.save()
        profile.save()

        return redirect('/'+user.userid)






    context = {}
    user = AuthUser.objects.get(userid = user_id)
    context['user'] = user 
    if user.is_student:
        profile = Student.objects.get(user = user)
        working = Working.objects.filter(user = user)
        context['working'] = working
        context['profile'] = profile
    else:
        profile = Teacher.objects.get(user = user)
        context['profile'] = profile

    endrosements = Endrosement.objects.filter(user = user)    
    context['endrosements'] = endrosements

    return render(request, 'profiles/edit.html',context)

# response of: example.com/userid/edit/endrosements
@login_required(login_url=var.LOGIN_URL)
def endrosement_add(request):

    if request.method == 'POST':
        form = EndrosementForm(request.POST)
        if form.is_valid():
            key = form.cleaned_data['key']
            value = form.cleaned_data['value']

            endrose = Endrosement()
            endrose.key = key
            endrose.value = value
            endrose.user = request.user 

            endrose.save()

        return redirect ('/'+request.user.userid)
    return HttpResponse('Invalid URL')




@login_required(login_url=var.LOGIN_URL)
def endrosement_delete(request, pk):
    if request.method == 'GET':
        return HttpResponse('Invalid Request')
    try:
        endrose = Endrosement.objects.get(pk = pk)
        if endrose.user == request.user:
            endrose.delete()
            return redirect('/'+request.user.userid)
        else:
            return HttpResponse('Invalid Request')
    except ObjectDoesNotExist as o:
        return HttpResponse('Invalid url')




@login_required(login_url=var.LOGIN_URL)
def endrosement_edit(request, pk):
    if request.method == 'POST':
        form = EndrosementForm(request.POST)
        if form.is_valid():
            key = form.cleaned_data['key']
            value = form.cleaned_data['value']

            try:
                endrose = Endrosement.objects.get(pk = pk)
                endrose.key = key
                endrose.value = value
                endrose.save()

                return redirect('/'+request.user.userid)
            except ObjectDoesNotExist as e:
                return HttpResponse('Invalid Request')
                

    else:
        try:
            endrose = Endrosement.objects.get(pk=pk)
            if endrose.user != request.user:
                return HttpResponse('Invalid Request')

            form = EndrosementForm()
            form.fields['key'].initial = endrose.key
            form.fields['value'].initial = endrose.value

            context = {
                'form' : form,
                'pk' : pk
            }

            return render(request, 'profiles/edit_endrosement.html', context)
        except ObjectDoesNotExist as e:
            return HttpResponse('Invalid URL')



# response of: example.com/userid/working/edit
@login_required(login_url=var.LOGIN_URL)
def working_add(request):

    if request.method == 'POST':
        form = WorkingForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data['company']
            position = form.cleaned_data['position']
            from_date = form.cleaned_data['from_date']
            current = form.cleaned_data['current']
            to_date = form.cleaned_data['to_date']
            comment = form.cleaned_data['comment']

            work = Working()
            work.company = company
            work.position = position
            work.from_date = from_date
            work.current = current
            if not current:
                work.to_date = to_date
            else:
                work.to_date = datetime.today()
            work.comment = comment
            work.user = request.user

            work.save()

            return HttpResponse('successfully saved')

        else:
            return HttpResponse('Not Working')


    form = WorkingForm()
    context = {
        'form' : form,
        'edit' : False
    }
    return render(request, 'profiles/edit_working.html',context)



@login_required(login_url=var.LOGIN_URL)
def working_edit(request, pk):
    
    if request.method == 'POST':
        form = WorkingForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data['company']
            position = form.cleaned_data['position']
            from_date = form.cleaned_data['from_date']
            current = form.cleaned_data['current']
            to_date = form.cleaned_data['to_date']
            comment = form.cleaned_data['comment']

            work = Working.objects.get(pk = pk)
            work.company = company
            work.position = position
            work.from_date = from_date
            work.current = current
            if not current:
                work.to_date = to_date
            work.comment = comment

            work.save()

            return HttpResponse('successfully saved')

        else:
            return HttpResponse('Not Working')

    try:
        work = Working.objects.get(pk = pk)

        form = WorkingForm()
        form.fields['company'].initial = work.company
        form.fields['position'].initial = work.position
        form.fields['from_date'].initial = work.from_date
        form.fields['current'].initial = work.current
        form.fields['to_date'].initial = work.to_date
        form.fields['comment'].initial = work.comment

        context = {
            'form' : form,
            'edit' : True,
            'pk' : pk
        }

        return render(request, 'profiles/edit_working.html', context)
    except ObjectDoesNotExist as e:
        return HttpResponse('Invalid Request')



# response of: example.com/userid/working/delete/pk/
@login_required(login_url=var.LOGIN_URL)
def working_delete(request, pk):
    if request.method == 'POST':
        try:
            work = Working.objects.get(pk = pk)
            if work.user != request.user:
                pass

            work.delete()
            return HttpResponse('Deleted')

        except ObjectDoesNotExist as e:
            pass


    return HttpResponse('Invalid Request')



# response of: example.com/feeds/
def feeds(request):

    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        file_data = request.FILES
        image_file = file_data.get('image')

        post = Post()

        if image_file != None:
            if Image.is_valid_format(image_file.name):

                # chunk the total stream for bufferring
                if image_file.multiple_chunks(2500000):
                    image_file.chunks(2500000)

                # read the image file stream
                bytes_data = image_file.read()
                imgsrc = Image.save(var.FOLDER_POST, bytes_data)
                post.imgsrc = imgsrc
                post.has_media = True
            else:
                post.has_media = False
        else:
            post.has_media = False

        post.title = title
        post.body = body
        post.user = request.user
        

        post.save()

    posts = Post.objects.order_by('time_date')[::-1]
    context = {
        'posts' : posts
        }
    return render(request, 'feeds.html', context)

@login_required(login_url = var.LOGIN_URL)
def feed_delete(request, pk):
    try:
        post = Post.objects.get(pk = pk)
        if post.has_media:
            Image.delete(post.imgsrc)
        post.delete()
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

