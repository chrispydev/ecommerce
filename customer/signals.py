from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from customer.models import Customer, Message
from store.textMessage import send_message


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
        send_message(message_body, to=to_phone_number)