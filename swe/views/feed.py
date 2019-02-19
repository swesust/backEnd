from django.contrib.auth.decorators import login_required
from django.contrib.postgres import search
from django.contrib.postgres.search import SearchVector
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, Paginator
from django.shortcuts import render, redirect,HttpResponse
from django.utils.timezone import now

from swe.helper import Image
from swe.models import Post
from swe import variables as var 

from .view import invalid

# response of: example.com/feeds/
def all(request):

    obj = Post.objects.order_by('time_date')[::-1]

    # max 10 page per page
    pages = Paginator(obj, 10)

    page = request.GET.get('page', 1)

    # try to render the page if exist
    try:
        posts = pages.get_page(page)
    except EmptyPage as e:
        return invalid(request)

    context = {
        'posts' : posts,
        'search' : False
        }
    return render(request, 'post/feeds.html', context)


def single(request, pk):
    try:
        post = Post.objects.get(pk = pk)
        context = {
            'post' : post
        }

        return render(request, 'post/single.html', context)
    except ObjectDoesNotExist as e:
        return invalid(request)


def search(request):

    if(request.method == 'GET'):
        query = request.GET.get('query',None)
        page = request.GET.get('page', 1)

    else:
        query = request.POST.get('query', None)
        page = request.POST.get('page', 1)

    if query is None:
        return invalid(request)

    result = Post.objects.annotate(search=SearchVector(
        'body', 'title')).filter(search=query)

    pages = Paginator(result, 1)

    try:
        page = int(page)
        posts = pages.page(page)
        context = {
            'posts' : posts,
            'search' : True,
            'query' : query
        }
        print(request.path)
        return render(request, 'post/feeds.html', context)
    except EmptyPage as e:
        return HttpResponse('Search Page Not Found')



@login_required(login_url = var.LOGIN_URL)
def create(request):

    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        file_data = request.FILES
        image_file = file_data.get('image')

        post = Post()

        if image_file != None:
            if Image.is_valid_format(image_file.name):
                # chunk the total stream for bufferring
                if image_file.multiple_chunks(var.FILE_CHUNK_SIZE):
                    image_file.chunks(var.FILE_CHUNK_SIZE)

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
        return redirect('/feeds/')

    context = {
        'edit' : False
    }
    return render(request, 'post/edit.html', context)
    

@login_required(login_url = var.LOGIN_URL)
def edit(request, pk):

    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        file_data = request.FILES
        image_file = file_data.get('image')

        post = Post.objects.get(pk = pk)

        if image_file != None:
            if Image.is_valid_format(image_file.name):

                # chunk the total stream for bufferring
                if image_file.multiple_chunks(var.FILE_CHUNK_SIZE):
                    image_file.chunks(var.FILE_CHUNK_SIZE)

                if post.has_media:
                    Image.delete(post.imgsrc)

                # read the image file stream
                bytes_data = image_file.read()
                imgsrc = Image.save(var.FOLDER_POST, bytes_data)
                post.imgsrc = imgsrc
                post.has_media = True

        post.title = title
        post.body = body
        post.time_date = now()
        post.user = request.user 
        post.save()

        return redirect('/feeds/')

    try:
        post = Post.objects.get(pk = pk)
        if post.user is not request.user:
            pass


        context = {
            'edit' : True,
            'post' : post
        }

        return render(request, 'post/edit.html', context)
    except ObjectDoesNotExist as e:
        pass

    return invalid(request)


@login_required(login_url = var.LOGIN_URL)
def delete(request, pk):
    try:
        post = Post.objects.get(pk = pk)
        if post.has_media:
            Image.delete(post.imgsrc)
            
        post.delete()
        # redirect to current page
        return redirect('/feeds/')
    except ObjectDoesNotExist as e:
        return invalid(request)

