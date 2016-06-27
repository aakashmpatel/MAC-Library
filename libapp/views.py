from django.shortcuts import render
import pprint
import random
# Create your views here.
from django.http import HttpResponse,Http404,HttpResponseRedirect
from libapp.models import Book, Dvd, LibUser, Libitem,Suggestion
from libapp.forms import SuggestionForm,SearchlibForm,LoginForm
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.
def index(request):
    # booklist = Book.objects.all() [:10]
    # dvdlist = Dvd.objects.all() [:5]
    # response = HttpResponse()
    # heading1 = '<p>' + 'List of books: ' + '</p>'
    # response.write(heading1)
    # for book in booklist:
    #     para = '<p>' + str(book) + '</p>'
    #     response.write(para)
    # heading2 = '<p>' + 'List of DVDs: ' + '</p>'
    # response.write(heading2)
    # sort = Dvd.objects.order_by('-pubyr')
    # for dvd in sort:
    #     para = '<p>' + str(dvd) + '</p>'
    #
    #     response.write(para)
    #
    # return response

    itemlist = Libitem.objects.all().order_by('title')[:10]

    return render(request, 'libapp/index.html', {'itemlist': itemlist,'name':request.user})

def about(request):
    visit = int(request.COOKIES.get('num','0'))
    visit = visit +1
    limit = 300
    response = render(request,'libapp/about.html',{'visit':visit})
    response.set_cookie('num',visit,max_age=limit)
    return response

def detail(request,item_id):

    # booklist = Book.objects.all()
    # dvdlist = Dvd.objects.all()
    # response = HttpResponse()
    # heading1 = '<p>' + 'List of Books/Dvd\'s' + '</p>'
    # response.write(heading1)
    # isBook = 0
    # isDvd = 0
    #
    # for book in booklist:
    #     # response.write(book.id)
    #     # response.write(item_id)
    #     if book.id == int(item_id):
    #         para = '<p>' + str(book.title)+' '+str(book.author)+' '+str(book.duedate)+' '+str(book.itemtype)+ '</p>'
    #         response.write(para)
    #         isBook = 1
    #         break
    #     else:
    #         isBook = 0
    #
    #
    #
    # for dvd in dvdlist:
    #     # response.write(isBook)
    #     if dvd.id == int(item_id):
    #         para = '<p>' + str(dvd.title)+' '+str(dvd.maker)+' '+str(dvd.duedate)+' '+str(dvd.itemtype)+ '</p>'
    #         response.write(para)
    #         isDvd = 1
    #         break
    #     else:
    #         isDvd = 0
    #
    # if(isBook == 0 and isDvd == 0):
    #     raise Http404
    booklist = Book.objects.all()
    dvdlist = Dvd.objects.all()
    itemlist = Libitem.objects.all()

    return render(request,'libapp/detail.html',{'item_id':item_id,'booklist':booklist,'dvdlist':dvdlist,'itemlist':itemlist})

def suggestions(request):
    suggestionlist = Suggestion.objects.all()[:10]
    return render(request, 'libapp/suggestions.html', {'itemlist': suggestionlist})

def newitem(request):
    suggestions = Suggestion.objects.all()
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.num_interested = 1
            suggestion.save()
            return HttpResponseRedirect(reverse('libapp:suggestions'))
        else:
            return render(request, 'libapp/newitem.html', {'form':form, 'suggestions':suggestions})
    else:
        form = SuggestionForm()
        return render(request, 'libapp/newitem.html', {'form':form, 'suggestions':suggestions})

def searchlib(request):

        form = SearchlibForm()
        if request.method == 'GET':
            return render(request, 'libapp/search.html', {'form': form})

        else:
            form = SearchlibForm()
            if request.POST.get("title") != '':
                q = request.POST.get("title")
                booklist = Book.objects.filter(title__contains=q)
                dvdlist = Dvd.objects.filter(title__contains=q)
                if request.POST.get("author") != '':
                    r = request.POST.get("author")
                    booklist = booklist.filter(author__contains=r)
                    dvdlist = dvdlist.filter(maker__contains=r)
                return render(request,'libapp/search.html',{'booklist':booklist,'dvdlist':dvdlist,'form':form})
            elif request.POST.get("author") != '':
                q = request.POST.get("author")
                booklist = Book.objects.filter(author__contains=q)
                dvdlist = Dvd.objects.filter(maker__contains=q)
                return render(request, 'libapp/search.html', {'booklist': booklist, 'dvdlist': dvdlist,'form':form})
            else:
                return render(request, 'libapp/search.html',{'form': form})




def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('libapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        form = LoginForm()
        luck_num = random.randint(1,9)
        request.session['luckynum'] = luck_num
        return render(request, 'libapp/login.html',{'form':form,'luckynum':luck_num})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('libapp:index')))


def register(request):
    return render(request,'libapp/register.html')

def myitems(request):
    if request.user.is_authenticated():
        checked_out = Libitem.objects.filter(checked_out=1).filter(user=request.user)
        return render(request,'libapp/myitems.html',{'checked_out':checked_out})
    else:
        return HttpResponse('You are not a LibUser')