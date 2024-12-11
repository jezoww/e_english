from django.urls import path

from apps.admin2.views import AdminPanelBookListView, AdminPanelBookCreateView, AdminPanelBookDeleteView, \
    AdminPanelBookUpdateView

urlpatterns = [
    path('book-list/', AdminPanelBookListView.as_view(), name='book-list'),
    path('book-create/', AdminPanelBookCreateView.as_view(), name='book-create'),
    path('book-delete/<int:pk>', AdminPanelBookDeleteView.as_view(), name='book-delete'),
    path('book-update/<int:pk>', AdminPanelBookUpdateView.as_view(), name='book-update'),
]