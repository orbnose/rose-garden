from django.shortcuts import render
from django.http import HttpResponse
from .models import Book

def homepage(request):
    context = {'book_list': Book.objects.all()}
    return render(request, 'rosegarden/index.html', context)
