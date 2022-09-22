from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Book, Branch, BranchUserProfile

def homepage(request):
    context = {'book_list': Book.objects.all().order_by('title')}
    return render(request, 'rosegarden/index.html', context)

def bookDetails(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    return render(request, 'rosegarden/bookDetails.html', {'book': book})

def search(request):
    return render(request, 'rosegarden/search.html')

def branchList(request):
    context = {'branch_list': Branch.objects.all().order_by('name')}
    return render(request, 'rosegarden/branchList.html', context)

def branchDetails(request, branch_pk):
    branch = get_object_or_404(Branch, pk=branch_pk)
    return render(request, 'rosegarden/branchDetails.html', {'branch': branch})

def userList(request):
    context = {'profile_list': BranchUserProfile.objects.all().order_by('user__username')}
    return render(request, 'rosegarden/userList.html', context)

def userDetails(request, username):
    content = 'User Page for ' + username
    return HttpResponse(content)

def add_book(request):
    content = 'Add Book Page'
    return HttpResponse(content)