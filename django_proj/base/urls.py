from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/<str:pk>/', views.books, name='books'),
    path('export-books-xml/', views.export_books_xml, name='export-books-xml'),
    path('export-books-xls/', views.export_books_xls, name='export-books-xls'),
    # path('admin/import-books-xml/', views.import_books_xml, name='import-books-xml'),

    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    
    path('donate-book/', views.donateBook, name='donate-book'),
    path('my-borrows/', views.userBorrows, name='my-borrows'),
    path('extend-borrow/<int:pk>/', views.extendBorrow, name='extend-borrow'),
    path('borrow-book', views.borrowBook, name='borrow-book')
]
