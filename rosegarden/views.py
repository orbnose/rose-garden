from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Book, Branch, BranchUserProfile
from .forms import BookForm

# -- Page Views -- 
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
    user = get_object_or_404(User, username=username)
    profile = BranchUserProfile.objects.get(user=user)
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'rosegarden/userDetails.html', context)

def add_book(request):
    content = 'Add Book Page'
    return HttpResponse(content)

def edit_book(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    
    #User is not authenticated
    if not request.user.is_authenticated:
        return HttpResponseForbidden('forbidden')

    #User does not point to a branch
    try:
        profile = BranchUserProfile.objects.get(user=request.user)
    except BranchUserProfile.DoesNotExist:
        return HttpResponseForbidden('forbidden')

    #User branch does not match the book's branch
    if not (profile.branch.pk == book.branch.pk):
        return HttpResponseForbidden('forbidden')

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('rosegarden:book_details', args=[book.pk]))
    else:
        form = BookForm(instance=book)
    
    context = {
        'book': book,
        'form': form,
        }
    return render(request, 'rosegarden/bookEdit.html', context)