from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Book, Branch, BranchUserProfile
from .forms import BookForm, UserProfileInterestsForm, QuickSearchForm, FullSearchForm

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
    matching_user = profile.matches_request_user(request)
    context = {
        'page_user': user,
        'username': username,
        'profile': profile,
        'matching_user': matching_user,
    }
    return render(request, 'rosegarden/userDetails.html', context)

def userEdit(request, username):
    page_user = get_object_or_404(User, username=username)
    page_profile = BranchUserProfile.objects.get(user=page_user)

    if page_profile is None:
        return HttpResponseForbidden('forbidden')
    
    if not page_profile.matches_request_user(request):
        return HttpResponseForbidden('forbidden')
    
    if request.method == 'POST':
        form = UserProfileInterestsForm(request.POST, instance=page_profile)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('rosegarden:user_details', args=[username]))
    else:
        form = UserProfileInterestsForm(instance=page_profile)
    
    context = {
        'username': username,
        'form': form,
    }
    return render(request, 'rosegarden/userEdit.html', context)

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

def get_no_results_flag(book_list):
    if book_list:
        return False
    else:
        return True

def quicksearch_books(query):
    return Book.objects.filter(
            Q(title__icontains=query) | 
            Q(author_editor__icontains=query) | 
            Q(branch__name__icontains=query) | 
            Q(version__icontains=query) | 
            Q(ddc_number__icontains=query)
        )

def fullsearch_books(querydict):
    logic = querydict["f"]
    title = querydict["title"]
    author = querydict["author"]
    ddcmin = querydict["ddcmin"]
    ddcmax = querydict["ddcmax"]
    category = querydict["cat"]
    is_bio = querydict["bio"]
    branch = querydict["branch"]
    queries = []
    query = Q()

    if title:
        queries.append( Q(title__icontains=title) )
    
    if author:
        queries.append( Q(author_editor__icontains=author) )

    # The category selector takes precedence over the DDC range search
    # Handle the case for the "000" category so that it doesn't get passed over when checking for existence
    if category=="000":
        category = "zero"

    if category:
        if category == "zero":
            ddcmin = "000.000000001"
            ddcmax = "099.999999999"
        else:
            # only keep the integer 100's place from the passed in category string
            ddcmin = int(category)
            ddcmax = ddcmin + 99.999999999

    if ddcmin and ddcmax:
        queries.append( Q(ddc_number__gte=ddcmin) & Q(ddc_number__lte=ddcmax) )
    elif ddcmin:
        queries.append( Q(ddc_number__gte=ddcmin) )
    elif ddcmax:
        queries.append( Q(ddc_number__lte=ddcmax) )
    
    if is_bio:
        queries.append( Q(is_biography_or_memoir__exact=is_bio) )

    if branch:
        queries.append( Q(branch__pk__exact=branch.pk) )
    
    for condition in queries:
        if logic == 'any':
            query |= condition
        else:
            query &= condition
    
    return Book.objects.filter(query)

def search(request):

    quicksearch_query = request.GET.get("q")
    fullsearch_logic = request.GET.get("f")

    if quicksearch_query:
        quicksearch_form_submitted = QuickSearchForm(request.GET)

        if quicksearch_form_submitted.is_valid():
            query = quicksearch_form_submitted.cleaned_data['q']
            book_list = quicksearch_books(query)
            no_results_flag = get_no_results_flag(book_list)
        else:
            book_list = False
            no_results_flag = False
        
        quicksearch_form = quicksearch_form_submitted
        fullsearch_form = FullSearchForm()

    elif fullsearch_logic == "all" or fullsearch_logic == "any":
        fullsearch_form_submitted = FullSearchForm(request.GET)

        if fullsearch_form_submitted.is_valid():
            querydict = fullsearch_form_submitted.cleaned_data
            book_list = fullsearch_books(querydict)
            no_results_flag = get_no_results_flag(book_list)
        else:
            book_list = False
            no_results_flag = False

        quicksearch_form = QuickSearchForm()
        fullsearch_form = fullsearch_form_submitted

    else:
        book_list = False
        no_results_flag = False
        quicksearch_form = QuickSearchForm()
        fullsearch_form = FullSearchForm()

    context = {
        'no_results_flag': no_results_flag,
        'book_list': book_list,
        'quicksearch_form': quicksearch_form,
        'fullsearch_form': fullsearch_form,
    }
    return render(request, 'rosegarden/search.html', context)