from django.forms import ModelForm
from .models import Book, Borrow
from django import forms
from datetime import datetime, timedelta

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'releaseYear']

class BorrowForm(ModelForm):
    class Meta:
        model = Borrow
        fields = ['book', 'endDate']
        widgets = {'endDate': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['book'].queryset = Book.objects.filter(borrowed=False)
        self.fields['endDate'].initial = datetime.now().date() + timedelta(days=14)

class ImportXMLForm(forms.Form):
    xml_file = forms.FileField(label='XML file')
        
# class BorrowForm(ModelForm):
#     class Meta:
#         model = Borrow
#         fields = ['book', 'endDate']

#         endDateChoices = [(14, '14 dni'), (28, '28 dni')]
#         widgets = {
#             'book': forms.Select(attrs={'class': 'form-control'}),
#             'endDate': forms.Select(choices=endDateChoices)
#         }

#     def clean_endDate(self):
#         # selected_days = int(self.data.get('endDate', 14))
#         selected_days = self.cleaned_data.get('endDate')
#         current_date = datetime.now().date()
#         end_date = current_date + timedelta(days=selected_days)
#         return end_date