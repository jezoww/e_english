from django.urls import path

from apps.admin2.views import AdminPanelVocabListView, AdminPanelVocabCreateView, AdminPanelVocabDeleteView, \
    AdminPanelVocabUpdateView, AdminPanelVocabCreateExcelView

urlpatterns = [
    path('vocab-list/', AdminPanelVocabListView.as_view(), name='vocab-list'),
    path('vocab-create/', AdminPanelVocabCreateView.as_view(), name='vocab-create'),
    path('vocab-delete/<int:pk>/', AdminPanelVocabDeleteView.as_view(), name='vocab-delete'),
    path('vocab-update/<int:pk>/', AdminPanelVocabUpdateView.as_view(), name='vocab-update'),
    path('vocab-create-excel/', AdminPanelVocabCreateExcelView.as_view(), name='vocab-create-excel'),
]


