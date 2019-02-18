from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render,redirect
from django.utils.timezone import datetime

from swe.forms import WorkingForm
from swe.models import Working
from swe import variables as var

from .view import invalid

# response of: example.com/userid/working/edit
@login_required(login_url=var.LOGIN_URL)
def add(request, user_id):

    if request.method == 'POST':
        form = WorkingForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data['company']
            position = form.cleaned_data['position']
            from_date = form.cleaned_data['from_date']
            current = form.cleaned_data['current']
            to_date = form.cleaned_data['to_date']
            country = form.cleaned_data['country']
            comment = form.cleaned_data['comment']

            work = Working()
            work.company = company
            work.position = position
            work.from_date = from_date
            work.current = current
            work.country = country
            if not current:
                work.to_date = to_date
            else:
                work.to_date = datetime.today()
            work.comment = comment
            work.user = request.user

            work.save()

            return redirect('/'+user_id)

        else:
            return invalid(request)


    form = WorkingForm()
    context = {
        'form' : form,
        'edit' : False
    }
    return render(request, 'profiles/edit_working.html',context)


@login_required(login_url=var.LOGIN_URL)
def edit(request, user_id, pk):
    
    if request.method == 'POST':
        form = WorkingForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data['company']
            position = form.cleaned_data['position']
            from_date = form.cleaned_data['from_date']
            current = form.cleaned_data['current']
            to_date = form.cleaned_data['to_date']
            country = form.cleaned_data['country']
            comment = form.cleaned_data['comment']

            work = Working.objects.get(pk = pk)
            work.company = company
            work.position = position
            work.from_date = from_date
            work.current = current
            work.country = country
            if not current:
                work.to_date = to_date
            work.comment = comment

            work.save()

            return redirect('/'+user_id)

        else:
            return invalid(request)

    try:
        work = Working.objects.get(pk = pk)

        form = WorkingForm()
        form.fields['company'].initial = work.company
        form.fields['position'].initial = work.position
        form.fields['from_date'].initial = work.from_date
        form.fields['current'].initial = work.current
        form.fields['to_date'].initial = work.to_date
        form.fields['comment'].initial = work.comment
        form.fields['country'].initial = work.country

        context = {
            'form' : form,
            'edit' : True,
            'pk' : pk
        }

        return render(request, 'profiles/edit_working.html', context)
    except ObjectDoesNotExist as e:
        return invalid(request)


# response of: example.com/userid/working/delete/pk/
@login_required(login_url=var.LOGIN_URL)
def delete(request, user_id, pk):
    if request.method == 'POST':
        try:
            work = Working.objects.get(pk = pk)
            if work.user != request.user:
                pass

            work.delete()
            return redirect('/'+user_id)

        except ObjectDoesNotExist as e:
            return invalid(request)

    return invalid(request)
