from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import BookForm, BorrowForm
from .models import Borrow
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from .models import Book
from openpyxl import Workbook

from .models import Book
# Create your views here.

def home(request):
    bookList = Book.objects.all()

    context = {'books':bookList}
    return render(request, 'base/home.html', context)

def books(request, pk):
    book = Book.objects.get(id = pk)

    context = {'book':book}
    return render(request, 'base/books.html', context)

@require_GET
def export_books_xml(request):
    books = Book.objects.all()

    xml_data = f'<?xml version="1.0" encoding="UTF-8"?><books>'

    for book in books:
        xml_data += f'<book><title>{book.title}</title><author>{book.author}</author><releaseYear>{book.releaseYear}</releaseYear></book>'

    xml_data += '</books>'

    response = HttpResponse(xml_data, content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename=books.xml'
    return response

@require_GET
def export_books_xls(request):
    books = Book.objects.all()

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(['Title', 'Author', 'Release Year'])
    for book in books:
        worksheet.append([book.title, book.author, book.releaseYear])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=books.xlsx'
    workbook.save(response)

    return response

def donateBook(request):
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Dziękujemy za dotacje książki')
            return redirect('home')
        

    context = {'form' : form}
    return render(request, 'base/book_form.html', context)

@login_required
def borrowBook(request):
    form = BorrowForm()
    if request.method == 'POST':
        form = BorrowForm(request.POST)
        
        if form.is_valid():
            borrow = form.save(commit=False)

            book = borrow.book

            borrow.user = request.user
            borrow.startDate = datetime.now().date()
            book.borrowed = True

            book.save()
            borrow.save()
            messages.info(request, 'Książka ' + str(book.title) + ' została wypożyczona')
            return redirect('home')
        
    context = {'form' : form}
    return render(request, 'base/borrow_form.html', context)

@login_required
def userBorrows(request):
    borrows = Borrow.objects.filter(user=request.user)

    context = {'borrows' : borrows}
    return render(request, 'base/user_borrows.html', context)

@login_required
def extendBorrow(request, pk):
    if request.method == 'POST':
        borrow = Borrow.objects.get(id=pk)
        borrow.endDate += timedelta(days=14)
        borrow.save()
        messages.info(request, 'Wyopożyczenie przedłużone')

    return redirect('my-borrows')

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'Użytkownik nie ustnieje')
    
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Użytkownik nie ustnieje lub hasło nie jest poprawne')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def registerPage(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Błąd')


    context = {'page' : page, 'form' : form}
    return render(request, 'base/login_register.html', context)

@login_required
def logoutUser(request):
    logout(request)
    return redirect('home')

