from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from apps.admin2.forms import UnitModelForm
from apps.user.models import Book, Unit


class AdminPanelUnitListView(ListView):
    queryset = Unit.objects.all()
    template_name = 'admin2/unit-list.html'
    context_object_name = 'units'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        return context

    def post(self, request):
        search = request.POST.get('search')
        if search.isdigit():
            units = Unit.objects.filter(unit_num=search)
        else:
            units = Unit.objects.filter(name__icontains=search)
        context = {'units': units}
        return render(request, 'admin2/unit-list.html', context=context)

    # def post(self, request):
    #     search = request.POST.get('search')
    #     if not search.isdigit():
    #         units = Unit.objects.filter(book__name__icontains=search)
    #     else:
    #         units = Unit.objects.filter(Q(book__level=search) | Q(book__name__icontains=search))
    #     data = []
    #     for unit in units:
    #         data.append({
    #             "id": unit.id,
    #             "name": unit.unit_num,
    #             "book": {
    #                 "id": unit.book.id,
    #                 "name": unit.book.name,
    #                 "level": unit.book.level
    #             }
    #         })
    #         return JsonResponse({"units": data})


class AdminPanelUnitCreateView(CreateView):
    model = Unit
    template_name = 'admin2/unit-list.html'
    form_class = UnitModelForm
    success_url = reverse_lazy('unit-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unit'] = Unit.objects.all()
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'Form data is not correct.')
        return super().form_invalid(form)


class AdminPanelUnitDeleteView(DeleteView):
    model = Unit
    template_name = 'admin2/admin-base.html'
    success_url = reverse_lazy('unit-list')
    pk_url_kwarg = 'pk'


class AdminPanelUnitUpdateView(UpdateView):
    model = Unit
    form_class = UnitModelForm
    success_url = reverse_lazy('unit-list')
    template_name = 'admin2/unit-list.html'


    def form_invalid(self, form):
        print(form)
