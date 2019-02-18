from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render,redirect

from swe.forms import EndrosementForm
from swe.helper import Image
from swe.models import (AuthUser, Student, Teacher, Endrosement, 
    Working, Post)
from swe import variables as var 

from .view import invalid

# response of: example.com/userid
def profile(request, user_id):
    """
    POST request
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
        posts = Post.objects.filter(user = user)

        endrose_form = EndrosementForm()
        context = {
            'user' : user,
            'profile' : profile,
            'is_auth' : is_auth,
            'is_self' : is_self,
            'endrosements' : endrosements,
            'endrose_form' : endrose_form,
            'posts' : posts
        }
        if user.is_student:
            # fetch all working information of this user
            works = Working.objects.filter(user=user).order_by('current', 'from_date')[::-1]
            context['works'] = works
            return render(request, 'profiles/student.html', context)
        else:
            return render(request, 'profiles/teacher.html', context)

    except ObjectDoesNotExist as e:
        return invalid(request)


# response of: example.com/userid/edit
@login_required(login_url=var.LOGIN_URL)
def edit(request, user_id):
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
            return invalid(request)

        elif user != request.user:
            return invalid(request)

        if user.is_student:
            profile = Student.objects.get(user = user)
        else:
            profile = Teacher.objects.get(user = user)

        files = request.FILES

        profile_img = files.get('profile_img')
        cover_img = files.get('cover_img')

        if profile_img != None:
            if Image.is_valid_format(profile_img.name):
                if profile_img.multiple_chunks(var.FILE_CHUNK_SIZE):
                    profile_img.chunks(var.FILE_CHUNK_SIZE)

                # remove the previous one
                Image.delete(profile.imgsrc)

                bytes_data = profile_img.read()
                if user.is_student:
                    profile.imgsrc = Image.save(var.FOLDER_STUDENT, bytes_data)
                else:
                    profile.imgsrc = Image.save(var.FOLDER_TEACHER, bytes_data)


        if cover_img != None:
            if Image.is_valid_format(cover_img.name):
                if cover_img.multiple_chunks(var.FILE_CHUNK_SIZE):
                    cover_img.chunks(var.FILE_CHUNK_SIZE)

                # remove the previous one
                Image.delete(profile.cover)

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