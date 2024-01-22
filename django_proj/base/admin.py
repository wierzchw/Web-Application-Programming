from django.contrib import admin
from .models import Book, Borrow
from .forms import ImportXMLForm 
from django.urls import reverse
from django.utils.html import format_html
from django.shortcuts import render, redirect
import xml.etree.ElementTree as ET
from django.http import HttpResponse  # Dodaj import

class BookImport(admin.ModelAdmin):
    change_list_template = 'admin/yourapp/model/change_list_import_xml.html'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('admin/import-books-xml/', self.import_xml_view, name='import_xml'),
        ]
        return custom_urls + urls

    def import_xml_view(self, request):
        if request.method == 'POST':
            form = ImportXMLForm(request.POST, request.FILES)
            if form.is_valid():
                xml_file = request.FILES['xml_file']
            
                tree = ET.parse(xml_file)
                root = tree.getroot()
                for element in root:
                    Book.objects.create(title=element.find('title').text, author=element.find('author').text, releaseYear=element.find('releaseYear'))

                self.message_user(request, "Dane z pliku XML zostały zaimportowane.")
                return redirect('admin')
        else:
            form = ImportXMLForm()
            context = self.admin_site.each_context(request)
            context['opts'] = self.model._meta
            context['form'] = form
            return render(request, 'admin/yourapp/model/import_xml.html', context)
 

    def import_xml_button(self, request, extra_context=None):
        return format_html('<a class="button" href="{}">{}</a>',
                           reverse('admin:import_xml'), 'Importuj XML')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['import_xml_button'] = self.import_xml_button(request)
        return super().changelist_view(request, extra_context=extra_context)


# admin.site.register(Book)
admin.site.register(Borrow)
admin.site.register(Book, BookImport)