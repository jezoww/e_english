from django.urls import path

from apps.admin2.views import TestSectionCreateView, TestCreateView, TestUpdateView
from apps.admin2.views.test import TestListView, TestDeleteView

urlpatterns = [
    path('test-list/', TestListView.as_view(), name='test-list'),
    path('create-test/', TestCreateView.as_view(), name='create-test'),
    path('create-test-section/', TestSectionCreateView.as_view(), name='create-test-section'),
    path('delete-test/<int:pk>', TestDeleteView.as_view(), name='delete-test'),
    path('update-test/<int:pk>', TestUpdateView.as_view(), name='update-test'),
]
