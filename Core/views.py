from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView,ListView,CreateView
from django.core.files.storage import FileSystemStorage
from .forms import BookForm
from .models import Book
from django.urls import reverse_lazy

# Create your views here.

def home(request):
    count=User.objects.count()
    return render(request,'home.html',{'count':count})

def SignUp(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form=UserCreationForm()
    return render(request,'registration/signup.html',{'form':form})

@login_required
def secret_page(request):
    return render(request,'secret_page.html')
@login_required
def upload(request):
    context={}
    if request.method=='POST':
        uploaded_files=request.FILES['document']
        storage=FileSystemStorage()
        name=storage.save(uploaded_files.name,uploaded_files)
        context['url']=storage.url(name)
    return render(request,'upload.html',context)
@login_required
def book_list(request):
    books=Book.objects.all()
    return render(request,'book_list.html',{'books':books})

@login_required
def upload_book(request):
    if request.method=='POST':
        form=BookForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form=BookForm()
    return render(request,'upload_book.html',{'form':form})

@login_required
def delete_book(request,pk):
    if request.method=='POST':
        book=Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')

#################Model View Tempalte#######################################
class booklistview(ListView):
    model=Book
    template_name='class_book_list.html'
    context_object_name='books'

class uploadbookview(CreateView):
    model=Book
    form_class=BookForm
    success_url=reverse_lazy('book_list_view')
    template_name='upload_book.html'
