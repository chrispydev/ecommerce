from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from customer.models import Customer, Message
from store.text_message import send_text_message
from phonenumbers import format_number, PhoneNumberFormat
from django.core.mail import send_mail


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_customer(sender, instance, **kwargs):
    instance.customer.save()

@receiver(post_save, sender=Message)
def send_message_on_save(sender, instance, created, **kwargs):
    if created:
        message_body = instance.message
        to_phone_number = instance.user.customer.phone_number
        to_email = instance.user.email
        # Convert PhoneNumber object to a string
        to_phone_number_str = format_number(to_phone_number, PhoneNumberFormat.E164)
        send_text_message(to_phone_number_str, message_body)
        send_mail('order info',message_body, 'info@remgeeshop.com', [to_email])