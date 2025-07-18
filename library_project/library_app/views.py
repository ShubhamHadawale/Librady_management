from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Member, Transaction
from .forms import BookForm, MemberForm, ImportBooksForm
import requests
from datetime import datetime

def dashboard(request):
    return render(request, 'library/dashboard.html')

def book_list(request):
    query = request.GET.get('q')
    books = Book.objects.all()
    if query:
        books = books.filter(title__icontains=query) | books.filter(authors__icontains=query)
    return render(request, 'library/book_list.html', {'books': books})

def book_add(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'library/book_form.html', {'form': form})

def import_books(request):
    form = ImportBooksForm(request.GET or None)
    books = []
    if form.is_valid():
        number = form.cleaned_data['number']
        title = form.cleaned_data.get('title', '')
        page = 1
        while len(books) < number:
            url = f"https://frappe.io/api/method/frappe-library?page={page}&title={title}"
            response = requests.get(url).json()
            for book_data in response['message']:
                books.append(Book(
                    title=book_data['title'],
                    authors=book_data['authors'],
                    isbn=book_data.get('isbn'),
                    publisher=book_data.get('publisher'),
                    pages=int(book_data.get('num_pages') or 0),
                    stock=1
                ))
                if len(books) >= number:
                    break
            page += 1
        Book.objects.bulk_create(books)
        return redirect('book_list')
    return render(request, 'library/import_books.html', {'form': form})

def member_list(request):
    return render(request, 'library/member_list.html', {'members': Member.objects.all()})

def member_add(request):
    form = MemberForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('member_list')
    return render(request, 'library/member_form.html', {'form': form})

def issue_book(request, book_id, member_id):
    book = get_object_or_404(Book, id=book_id)
    member = get_object_or_404(Member, id=member_id)
    if book.stock > 0 and member.outstanding_debt <= 500:
        Transaction.objects.create(book=book, member=member)
        book.stock -= 1
        book.save()
    return redirect('dashboard')

def return_book(request, transaction_id):
    txn = get_object_or_404(Transaction, id=transaction_id)
    if txn.return_date is None:
        txn.return_date = datetime.today()
        txn.fee_charged = 10  # example fee
        txn.member.outstanding_debt += txn.fee_charged
        txn.member.save()
        txn.book.stock += 1
        txn.book.save()
        txn.save()
    return redirect('dashboard')
