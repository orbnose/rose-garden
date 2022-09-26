from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Book, Branch, BranchUserProfile
from .forms import BookForm

#______________________
#-- Helper Functions --

def get_user_branch_profile_from_request(request):
    #return the user branch if it exists, otherwise return None

    #User is not authenticated
    if not request.user.is_authenticated:
        return None
    
    #User does not have a profile
    try:
        profile = BranchUserProfile.objects.get(user=request.user)
    except BranchUserProfile.DoesNotExist:
        return None
 
    #Profile does not point to a branch
    if not profile.branch:
        return None

    return profile

#_________________
# -- Page Views --

def homepage(request):
    context = {'book_list': Book.objects.all().order_by('title')}
    return render(request, 'rosegarden/index.html', context)

def bookDetails(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    profile = get_user_branch_profile_from_request(request)
    
    if not profile:
        can_view_edit_button = False
    else:
        can_view_edit_button = profile.can_edit_book(book)
    
    context = {
        'can_view_edit_button': can_view_edit_button,
        'book': book
    }

    return render(request, 'rosegarden/bookDetails.html', context)

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
    profile = get_user_branch_profile_from_request(request)
    if profile is None:
        return HttpResponseForbidden('forbidden')

    if request.method== 'POST':
        form = BookForm(request.POST)

        if form.is_valid():
            book = form.instance
            book.branch = profile.branch
            book.save()
            return HttpResponseRedirect(reverse('rosegarden:book_details', args=[book.pk]))
    else:
        form = BookForm()
    
    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'rosegarden/bookAdd.html', context)

def edit_book(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    
    profile = get_user_branch_profile_from_request(request)
    if profile is None:
        return HttpResponseForbidden('forbidden')

    if not profile.can_edit_book(book):
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

def search(request):
    query = request.GET.get("q")
    if query:
        book_list = Book.objects.filter(
            Q(title__icontains=query) | Q(author_editor__icontains=query) | Q(branch__name__icontains=query) | Q(version__icontains=query) | Q(ddc_number__icontains=query)
        )
    else:
        book_list = False
    return render(request, 'rosegarden/search.html', {'book_list': book_list})