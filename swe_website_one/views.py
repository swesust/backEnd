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


def registration(request):
    return render(request, 'registration.html', {})