from django.urls import path

from apps.admin2.views import AdminPanelUnitListView, AdminPanelUnitCreateView, AdminPanelUnitDeleteView, \
    AdminPanelUnitUpdateView

urlpatterns = [
    path('unit-list/', AdminPanelUnitListView.as_view(), name='unit-list'),
    path('unit-create/', AdminPanelUnitCreateView.as_view(), name='unit-create'),
    path('unit-delete/<int:pk>', AdminPanelUnitDeleteView.as_view(), name='unit-delete'),
    path('unit-update/<int:pk>', AdminPanelUnitUpdateView.as_view(), name='unit-update'),
]
