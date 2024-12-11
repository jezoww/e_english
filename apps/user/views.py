from datetime import timedelta
from random import randint

import redis
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView, ListView
from redis import Redis

from apps.user.forms import LoginForm
from apps.user.models import User, Vocabulary, Unit, Result, Test, TestSection
from apps.user.tasks import send_verify_code


class IndexTemplateView(TemplateView):
    template_name = 'user/index.html'


class RegisterView(View):
    def get(self, request):
        return render(request, 'user/register/register.html')

    def post(self, request):
        r = redis.Redis()
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('register')
        code = randint(100000, 999999)
        send_verify_code.delay(email, code)
        r.mset({email: code})
        r.expire(email, timedelta(minutes=5))
        # request.session['hashC'] = make_password(str(code))
        request.session['email'] = email
        return redirect('check_code')


class LoginFormView(FormView):
    template_name = 'user/login/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        for e in form.errors.values():
            messages.error(self.request, e)
        return super().form_invalid(form)


class CheckCodeView(View):
    def get(self, request):
        email = request.session['email']
        context = {'email': email}
        return render(request, 'user/register/check_code.html', context)

    def post(self, request):
        r = redis.Redis(decode_responses=True)
        code1 = request.POST.get('code')
        email = request.session['email']
        code2 = r.mget(email)[0]
        if code2:
            if int(code1) == int(code2):
                return redirect('set_password')
            r.delete(email)
        messages.error(request, 'Incorrect code, we sent other code! Check one more time!')
        code = randint(100000, 999999)
        send_verify_code.delay(email, code)
        r.mset({email: code})
        r.expire(email, timedelta(minutes=5))
        request.session['email'] = email

        return redirect('check_code')


class SetPasswordView(View):
    def get(self, request):
        return render(request, 'user/register/set_password.html')

    def post(self, request):
        password = request.POST.get('password')
        password = make_password(password)
        email = request.session['email']
        User.objects.create(email=email, password=password)
        request.session.pop('email', None)
        messages.success(request, 'Successfully registered!')
        return redirect('login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class ForgotPassword(View):
    def get(self, request):
        return render(request, 'user/login/forgot_password.html')

    def post(self, request):
        r = redis.Redis()
        email = request.POST['email']
        if not User.objects.filter(email=email).exists():
            messages.error(request, 'Email not found!')
            return redirect('forgot_password')
        code = randint(100000, 999999)
        send_verify_code.delay(email, code)
        r.mset({email: code})
        r.expire(email, timedelta(minutes=5))
        # request.session['hashC'] = make_password(str(code))
        request.session['email'] = email
        return redirect('forgot_password_check_code')


class ForgotPasswordCheckCodeView(View):
    def get(self, request):
        email = request.session['email']
        context = {'email': email}
        return render(request, 'user/login/check_code_forgot_password.html', context)

    def post(self, request):
        r = redis.Redis(decode_responses=True)
        code1 = request.POST.get('code')
        email = request.session['email']
        code2 = r.mget(email)[0]
        if code2:
            if int(code1) == int(code2):
                return redirect('forgot_password_set_password')
            r.delete(email)
        messages.error(request, 'Incorrect code, we sent other code! Check one more time!')
        code = randint(100000, 999999)
        send_verify_code.delay(email, code)
        r.mset({email: code})
        r.expire(email, timedelta(minutes=5))
        request.session['email'] = email

        return redirect('forgot_password_check_code')


class ForgotPasswordSetPasswordView(View):
    def get(self, request):
        return render(request, 'user/login/set_password_forgot_password.html')

    def post(self, request):
        password = request.POST.get('password')
        password = make_password(password)
        email = request.session['email']
        user = User.objects.get(email=email)
        user.password = password
        user.save()
        request.session.pop('email', None)
        messages.success(request, 'Password successfully changed!')
        return redirect('login')


class UnitFilterListView(ListView):
    template_name = 'user/essential.html'
    context_object_name = 'vocabs'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['units'] = Unit.objects.all()
        return context

    def get_queryset(self):
        vocabs = cache.get('vocab_list')
        if not vocabs:
            vocabs = Vocabulary.objects.select_related('unit__book').order_by('id').all()
            cache.set('vocab_list', vocabs, timeout=60 * 60 * 24)
        return vocabs

    def post(self, request, *args, **kwargs):
        unit_id = request.POST.get('unit_id')
        if not unit_id:
            return JsonResponse({"success": False, "error": "Mavzu tanlanmagan."}, status=400)

        vocabs = Vocabulary.objects.filter(unit__id=unit_id).values("english", "uzbek", "audio__url")
        return JsonResponse({"success": True, "vocabs": list(vocabs)})


class CheckVocabView(View):
    def get(self, request):
        pass

    def post(self, request):
        r = Redis(decode_responses=True)
        vocab_id = request.POST.get('vocab')
        word = request.POST.get('word')
        vocab = Vocabulary.objects.get(id=vocab_id)
        r.mset({f"user:{request.user.id}:correct": 0,
                f"user:{request.user.id}:incorrect": 0,
                f"user:{request.user.id}:unit_id": vocab.unit_id})
        if word.isdigit():
            messages.error(request, 'Please do not enter a number.')
            return redirect('essential')
        if vocab.english.lower() == word.lower():
            messages.success(request, 'Correct!')
            r.incrby(f"user:{request.user.id}:correct", 1)
        else:
            messages.error(request, 'Incorrect!')
            r.decrby(f"user:{request.user.id}:incorrect", 1)
        correct = r.mget(f"user:{request.user.id}:correct")
        incorrect = r.mget(f"user:{request.user.id}:incorrect")
        context = {'correct': correct, 'incorrect': incorrect}
        return render(request, 'test.html', context=context)


class UnitTryView(View):
    def get(self, request):
        return render(request, 'test.html')

    def post(self, request):
        quantity = request.POST.get('quantity')
        typee = request.POST.get('type')
        book_id = request.POST.get('book')
        list_of_units = request.POST.getlist('unit')
        vocabs = Vocabulary.objects.filter(unit_id__in=list_of_units).order_by('?')[:quantity]
        context = {'vocabs': vocabs, 'type': typee}
        return render(request, 'test.html', context=context)


class SaveUnitResult(View):
    def post(self, request):
        r = Redis()
        user = request.user
        unit = r.mget(f"user:{request.user.id}:unit_id")
        correct = r.mget(f"user:{request.user.id}:correct")
        incorrect = r.mget(f"user:{request.user.id}:incorrect")
        Result.objects.create(user=user, unit=unit, correct=correct, incorrect=incorrect)
        return render(request, 'test.html')


class TestListView(ListView):
    template_name = 'user/tests.html'
    model = TestSection
    context_object_name = 'tests'


class TestDetailView(View):
    def get(self, request, pk):
        tests = Test.objects.filter(test_section_id=pk).values(
            'question', 'a', 'b', 'c', 'd', 'correct'
        )
        return JsonResponse(list(tests), safe=False)


from django.http import JsonResponse
from django.views import View
from apps.user.models import Vocabulary
import redis


class StartTestView(View):
    def post(self, request):
        r = redis.Redis(decode_responses=True)
        unit_id = request.POST.get('unit_id')
        quantity = int(request.POST.get('quantity'))
        test_type = request.POST.get('type_of_test')

        if not unit_id or not quantity:
            return JsonResponse({"success": False, "error": "Unit yoki savollar soni tanlanmagan."}, status=400)

        questions = Vocabulary.objects.filter(unit_id=unit_id).order_by('?')[:quantity]
        question_list = []

        for q in questions:
            question_list.append({
                "id": q.id,
                "english": q.english,
                "uzbek": q.uzbek,
                "audio": q.audio.url if q.audio else None
            })

        r.set(f"user:{request.user.id}:current_test", str(question_list), ex=3600)
        r.set(f"user:{request.user.id}:correct", 0)
        r.set(f"user:{request.user.id}:incorrect", 0)

        return JsonResponse({"success": True, "questions": question_list, "test_type": test_type})


class CheckAnswerView(View):
    def post(self, request):
        r = redis.Redis(decode_responses=True)
        question_id = request.POST.get('question_id')
        answer = request.POST.get('answer')

        question = Vocabulary.objects.get(id=question_id)

        if question.english.lower() == answer.lower():
            r.incr(f"user:{request.user.id}:correct")
            return JsonResponse({"success": True, "correct": True})
        else:
            r.incr(f"user:{request.user.id}:incorrect")
            return JsonResponse({"success": True, "correct": False})


class ShowResultView(View):
    def get(self, request):
        r = redis.Redis(decode_responses=True)
        correct = r.get(f"user:{request.user.id}:correct") or 0
        incorrect = r.get(f"user:{request.user.id}:incorrect") or 0

        return JsonResponse({"success": True, "correct": correct, "incorrect": incorrect})
