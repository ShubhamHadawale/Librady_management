from django import forms
from .models import Book, Member

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'

class ImportBooksForm(forms.Form):
    number = forms.IntegerField(min_value=1, max_value=100)
    title = forms.CharField(required=False)
