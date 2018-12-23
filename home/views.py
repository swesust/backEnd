from django.shortcuts import render


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
    return render(request, 'index.html', {})

def faculty(request):
    return render(request, 'faculty.html', {})

def login(request):
    if request.method == 'POST':
        print('post method')
        uid = request.POST.get('uid')
        password = request.POST.get('password')
        faculty = request.POST.get('faculty')
        print(uid, password, faculty)

        if faculty == None:
            print('student login ')
        else:
            print('faculty login')

        return render(request, 'login.html', {})
        
    else:
        print('get method')    
        return render(request, 'login.html', {})


def batchlist(request):
    return render(request, 'batchlist.html', {})

def batch(request, batch_id):
    context = {'batch_id' : batch_id,}
    return render(request, 'batch.html', context)