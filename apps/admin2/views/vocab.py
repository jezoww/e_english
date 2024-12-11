from django.contrib import messages
from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from apps.admin2.forms import VocabModelForm, VocabExcelForm
from apps.user.models import Vocabulary, Unit


class AdminPanelVocabListView(ListView):
    template_name = 'admin2/vocab-list.html'
    context_object_name = 'vocabs'
    paginate_by = 20

    def get_queryset(self):
        vocabs = cache.get('vocab_list')
        if not vocabs:
            vocabs = Vocabulary.objects.select_related('unit__book').order_by('id').all()
            cache.set('vocab_list', vocabs, timeout=60 * 60 * 24)
        return vocabs

    def post(self, request):
        search = request.POST.get('search')
        vocabs = Vocabulary.objects.filter(Q(uzbek__icontains=search) | Q(english__icontains=search))
        context = {'vocabs': vocabs}
        return render(request, 'admin2/vocab-list.html', context=context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['units'] = Unit.objects.all()
        return context


class AdminPanelVocabCreateView(CreateView):
    model = Vocabulary
    template_name = 'admin2/vocab-list.html'
    form_class = VocabModelForm
    success_url = reverse_lazy('vocab-list')

    def form_valid(self, form):
        form.save()
        cache.delete('vocab_list')
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return super().form_invalid(form)


class AdminPanelVocabDeleteView(DeleteView):
    model = Vocabulary
    pk_url_kwarg = 'pk'
    template_name = 'admin2/vocab-list.html'
    success_url = reverse_lazy('vocab-list')


class AdminPanelVocabUpdateView(UpdateView):
    pk_url_kwarg = 'pk'
    model = Vocabulary
    template_name = 'admin2/vocab-list.html'
    form_class = VocabModelForm
    success_url = reverse_lazy('vocab-list')


class AdminPanelVocabCreateExcelView(View):
    def get(self, request):
        return redirect('vocab-list')

    def post(self, request):
        form = VocabExcelForm(request.POST, request.FILES)
        if form.is_valid():
            return redirect('vocab-list')
        for error in form.errors.values():
            messages.error(request, error)
        return redirect('vocab-list')
