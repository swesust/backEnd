from django.contrib.postgres import search
from django.contrib.postgres.search import SearchVector
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponse,render
from django.template import loader

from swe.forms import SearchForm
from swe.models import (Batch,Student,Teacher,Working)


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


# response of: example.com/batch/	
def batchlist(request):
    """
    retrieve all the rows from `batch` table and make a dictionary
    and render the template with that dictionary
    """
    queryset = Batch.objects.all()[::-1]
    form = SearchForm()
    context = {
        'queryset' : queryset,
        'form' : form
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
        return invalid(request)

# custom error request response
def error404(request):
    context = {}
    return render(request, 'error404.html', context)


def search(request):
    if request.method == 'POST':
        context = {
            'found' : False
        }
        form = SearchForm(request.POST)
        if form.is_valid():
            current = form.cleaned_data['current']
            country = form.cleaned_data['country']
            company = form.cleaned_data['company']

            # unique query result using distinct
            if len(company) is 0:
                res = Working.objects.filter(country=country, current=current).distinct('user')
            else:
                res = Working.objects.filter(country=country, current=current, 
                    company__iexact=company).distinct('user')
            if res.exists():
                context['found'] = True
                context['res'] = res
                return render(request, 'search.html', context)


        return render(request, 'search.html', context)
    else:
        return invalid(request)


def invalid(request):
    response = loader.get_template('invalid.html');
    return HttpResponse(response.render({}, request))