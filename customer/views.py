from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth import login
from customer.models import Message
from store.models import Order
from django.contrib.auth.models import User
from customer.forms import UserRegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from customer.forms import UserUpdateForm, CustomerUpdateForm

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


class AccountView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        last_message = Message.objects.filter(user=user).order_by('-date_received').first()
        last_order = Order.objects.filter(user=user).order_by('-created_at').first()

        context = {
            'last_message': last_message,
            'last_order': last_order
        }

        return render(request, template_name='customer/account.html', context=context)

class ProfileView(View, LoginRequiredMixin):
    def post(self, request):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        c_form = CustomerUpdateForm(
            request.POST,instance=request.user.customer)
        if u_form.is_valid() and c_form.is_valid():
            u_form.save()
            c_form.save()
            return redirect('profile')
        else:
            template_name = 'customer/profile.html'
            context = {
                'u_form': u_form,
                'c_form': c_form,
            }
            return render(request, template_name, context)

    def get(self, request):
        u_form = UserUpdateForm(instance=request.user)
        c_form = CustomerUpdateForm(instance=request.user.customer)
        template_name = 'customer/profile.html'
        context = {
            'u_form': u_form,
            'c_form': c_form,
        }

        return render(request, template_name, context)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    context_object_name = 'inbox_messages'
    template_name = 'customer/message.html'
    ordering = ['-date_received']
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().filter(user=user)

        return queryset


class CustomPasswordResetDoneView(PasswordResetView):
    template_name = 'customer/password_reset.html'

    def form_valid(self, form):
        # Check if the email address is registered
        email = form.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()  # Replace User with your User model

        if user is None:
            # Display an alert or flash message
            messages.warning(self.request, 'The provided email address is not registered.')
            return redirect('password_reset')


        return super().form_valid(form)

