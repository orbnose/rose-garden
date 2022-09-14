from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Book, Branch, Copy

def homepage(request):
    context = {'book_list': Book.objects.all().order_by('title')}
    return render(request, 'rosegarden/index.html', context)

def bookDetails(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    return render(request, 'rosegarden/bookDetails.html', {'book': book})

def search(request):
    return render(request, 'rosegarden/search.html')

def branchList(request):
    return HttpResponse('Branch List')

def branchDetails(request, branch_pk):
    branch = get_object_or_404(Branch, pk=branch_pk)
    content = 'Branch Page for ' + branch.name
    return HttpResponse(content)

def userList(request):
    return HttpResponse('User List')

def userDetails(request, username):
    content = 'User Page for ' + username
    return HttpResponse(content)

def admin(request):
    return HttpResponse('Admin Login')
