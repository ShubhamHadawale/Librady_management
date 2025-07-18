from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.book_add, name='book_add'),
    path('books/import/', views.import_books, name='import_books'),
    path('members/', views.member_list, name='member_list'),
    path('members/add/', views.member_add, name='member_add'),
    path('issue/<int:book_id>/<int:member_id>/', views.issue_book, name='issue_book'),
    path('return/<int:transaction_id>/', views.return_book, name='return_book'),
]
