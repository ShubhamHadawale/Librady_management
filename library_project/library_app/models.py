from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    outstanding_debt = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    pages = models.IntegerField(default=0)
    stock = models.IntegerField(default=1)

    def __str__(self):
        return self.title

class Transaction(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(default=timezone.now)
    return_date = models.DateField(null=True, blank=True)
    fee_charged = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    def __str__(self):
        return f'{self.member.name} - {self.book.title}'
