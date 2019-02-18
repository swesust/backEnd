from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render,redirect

from swe.forms import EndrosementForm
from swe.models import Endrosement
from swe import variables as var

from .view import invalid 

# response of: example.com/userid/edit/endrosements
@login_required(login_url=var.LOGIN_URL)
def add(request, user_id):

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
    return invalid(request)


@login_required(login_url=var.LOGIN_URL)
def delete(request, user_id, pk):
    if request.method == 'GET':
        return invalid(request)
    try:
        endrose = Endrosement.objects.get(pk = pk)
        if endrose.user == request.user:
            endrose.delete()
            return redirect('/'+request.user.userid)
        else:
            return invalid(request)
    except ObjectDoesNotExist as o:
        return invalid(request)


@login_required(login_url=var.LOGIN_URL)
def edit(request, user_id, pk):
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
                return invalid(request)
                

    else:
        try:
            endrose = Endrosement.objects.get(pk=pk)
            if endrose.user != request.user:
                return invalid(request)

            form = EndrosementForm()
            form.fields['key'].initial = endrose.key
            form.fields['value'].initial = endrose.value

            context = {
                'form' : form,
                'pk' : pk
            }

            return render(request, 'profiles/edit_endrosement.html', context)
        except ObjectDoesNotExist as e:
            return invalid(request)