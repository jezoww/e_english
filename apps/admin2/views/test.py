from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from apps.admin2.forms import TestSectionModelForm, TestModelForm
from apps.user.models import Test, TestSection


class TestListView(ListView):
    model = Test
    template_name = 'admin2/test-list.html'
    context_object_name = 'tests'

    def get_context_data(self, **kwargs):
        context = super(TestListView, self).get_context_data(**kwargs)
        context['test_sections'] = TestSection.objects.all()
        return context


class TestSectionCreateView(CreateView):
    model = Test
    template_name = 'admin2/test-list.html'
    form_class = TestSectionModelForm
    success_url = reverse_lazy('test-list')


class TestCreateView(CreateView):
    model = Test
    template_name = 'admin2/test-list.html'
    form_class = TestModelForm
    success_url = reverse_lazy('test-list')


class TestDeleteView(DeleteView):
    template_name = 'admin2/test-list.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('test-list')
    model = Test


class TestUpdateView(UpdateView):
    template_name = 'admin2/test-list.html'
    pk_url_kwarg = 'pk'
    form_class = TestModelForm
    success_url = reverse_lazy('test-list')
    model = Test
