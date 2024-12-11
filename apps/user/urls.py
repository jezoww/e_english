from django.urls import path

from apps.user.views import TestListView, TestDetailView, StartTestView, CheckAnswerView, ShowResultView
from apps.user.views import IndexTemplateView, LoginFormView, RegisterView, CheckCodeView, SetPasswordView, LogoutView, \
    ForgotPassword, ForgotPasswordCheckCodeView, ForgotPasswordSetPasswordView, UnitFilterListView, CheckVocabView

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('check_code/', CheckCodeView.as_view(), name='check_code'),
    path('set_password/', SetPasswordView.as_view(), name='set_password'),
    path('forgot_password/', ForgotPassword.as_view(), name='forgot_password'),
    path('forgot_password_check_code/', ForgotPasswordCheckCodeView.as_view(), name='forgot_password_check_code'),
    path('forgot_password_set_password/', ForgotPasswordSetPasswordView.as_view(), name='forgot_password_set_password'),
]

urlpatterns += [
    path('essential/', UnitFilterListView.as_view(), name='essential'),
    path('check-vocabulary/', CheckVocabView.as_view(), name='check_vocab'),
]

urlpatterns += [
    path('tests/', TestListView.as_view(), name='tests'),
    path('test/<int:pk>/', TestDetailView.as_view(), name='test-detail'),
    path('start-test/', StartTestView.as_view(), name='start-test'),
    path('check-answer/', CheckAnswerView.as_view(), name='check-answer'),
    path('show-result/', ShowResultView.as_view(), name='show-result'),
]
