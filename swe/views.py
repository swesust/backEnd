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

from django.contrib.auth import authenticate

# Create your views here.


def home(request):
    if request.method == "POST":
        reg_no = request.POST['reg_no']
        email = request.POST['email']
        print("Reg No:", reg_no)
        print("Email: ", list(email))
        return render(request, 'bulma.html',{})
    return render(request, 'home.html', {})

def bulma(request):
    return render(request, 'bulma.html', {})


def index(request):
    print(request.user)
    print(request.user.is_authenticated)
    return render(request, 'index.html', {})

def faculty(request):

    try:
        print(request.user)
        print(request.user.is_anonymous)
        print(request.user.is_active)
    except Exception as e:
        raise e
    teachers = Teacher.objects.all()
    context = {'teachers' : teachers }
    return render(request, 'faculty.html', context)

def login(request):
    # user request for log
    if request.method == 'POST':
        uid = request.POST.get('uid')
        password = request.POST.get('password')
        
        user = authenticate(userid=uid, password=password)
        if user is not None:
            return render(request, 'index.html')

        else:
            return redirect('/login/')
        
    else:
        print('get method')    
        return render(request, 'login.html', {})


def batchlist(request):
    queryset = Batch.objects.all()
    context = {
        'queryset' : queryset,
    }
    return render(request, 'batchlist.html', context)

def batch(request, batch_id):
    try:
        batch = Batch.objects.get(year=batch_id)
        
        # fetch all students with batch year and sorting with reg id in ascending order
        students = Student.objects.filter(batch=batch_id).order_by('regid')
        context = {
            'batch' : batch, 
            'students' : students}
        return render(request, 'batch.html', context)

    except ObjectDoesNotExist as e:
        return render(request, 'error404.html', {})
        

def profile(request, user_id):

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



def error404(request):
    context = {}
    if request.method == 'POST':
        data = request.FILES
        imgsrc = data.get('profile')
        if imgsrc != None:
            print(type(imgsrc))
            #TemporaryUploadedFile(imgsrc)
            #print(imgsrc.temporary_file_path())
            print(imgsrc.name)

            print(Image.isValidFormat(imgsrc.name))

            # from name check the file format : jpg, jpeg, .png
            print(imgsrc.size)
            if imgsrc.multiple_chunks(2500000):
                imgsrc.chunks(2500000)

            r = imgsrc.read()
            #print('image loaded: ',r)
            print('loaded type: ', type(r))
            print('byte len: ',len(r))

            print('read file: ',type(r))

          
            img = ImageProcess.open(BytesIO(r))
            print(img.format)
            print(type(img.format))

    elif request.method == 'GET':

        loc = FSS(location='./media/user/')
        context = {'image' : '' }
        print(context['image'])
    

    return render(request, 'error404.html', context)


from django.contrib.auth import authenticate
def test(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        password = request.POST.get('password')


    return render(request, 'error404.html');