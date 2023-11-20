from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import login
from customer.forms import UserRegisterForm

class RegisterForm(View):
    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('product_home')
        else:
            user_form = UserRegisterForm()  # Create a new form instance
            template_name = 'customer/register.html'
            return render(request, template_name, {'user_form': user_form, 'form': form})

    def get(self, request):
        user_form = UserRegisterForm()
        template_name = 'customer/register.html'
        return render(request, template_name, {'user_form': user_form})
