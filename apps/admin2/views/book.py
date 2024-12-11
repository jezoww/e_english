from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from apps.admin2.forms import BookModelForm
from apps.user.models import Book


class AdminPanelBookListView(ListView):
    queryset = Book.objects.all()
    template_name = 'admin2/book-list.html'
    context_object_name = 'books'

    def post(self, request):
        search = request.POST.get('search')
        if not search.isdigit():
            books = Book.objects.filter(name__icontains=search)
        else:
            books = Book.objects.filter(Q(level=search) | Q(name__icontains=search))
        context = {'books': books}
        return render(request, 'admin2/book-list.html', context=context)


class AdminPanelBookCreateView(CreateView):
    model = Book
    template_name = 'admin2/book-list.html'
    form_class = BookModelForm
    success_url = reverse_lazy('book-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        return context


    def form_invalid(self, form):
        messages.error(self.request, 'Form data is not correct.')
        return super().form_invalid(form)


class AdminPanelBookDeleteView(DeleteView):
    model = Book
    template_name = 'admin2/book-list.html'
    success_url = reverse_lazy('book-list')
    pk_url_kwarg = 'pk'


class AdminPanelBookUpdateView(UpdateView):
    queryset = Book.objects.all()
    form_class = BookModelForm
    success_url = reverse_lazy('book-list')
    template_name = 'admin2/book-list.html'

