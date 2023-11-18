from django.shortcuts import render, HttpResponse,redirect
from django.views import View
from django.contrib import messages
from customer.forms import UserRegisterForm

class RegisterForm(View):
    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('product_home')
        else:
            return redirect('register')

    def get(self, request):
        user_form = UserRegisterForm()
        template_name = 'customer/register.html'
        return render(request, template_name, {'user_form': user_form})