from django.urls import path

from apps.admin2.views import AdminPanelTemplateView

urlpatterns = [
    path('panel/', AdminPanelTemplateView.as_view(), name='panel'),
]