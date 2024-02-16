from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.core.files.storage import default_storage

from store.models import Product

@receiver(pre_save, sender=Product)
def delete_old_product_image(sender, instance, **kwargs):
    if instance.id:
        try:
            old_product = Product.objects.get(id=instance.id)
            if old_product.product_image != instance.product_image and old_product.product_image.name != 'default.jpg':
                delete_file_from_storage(old_product.product_image.name)
        except Product.DoesNotExist:
            pass

@receiver(pre_delete, sender=Product)
def delete_product_media(sender, instance, **kwargs):
    # Delete the associated media file
    if instance.product_image:
        delete_file_from_storage(instance.product_image.name)

def delete_file_from_storage(file_path):
    if default_storage.exists(file_path):
        default_storage.delete(file_path)



# My code for local media files
# from django.db.models.signals import pre_delete, pre_save
# from django.dispatch import receiver
# from django.core.files.storage import default_storage

# from store.models import Product

# @receiver(pre_save, sender=Product)
# def delete_old_product_image(sender, instance, **kwargs):
#     if instance.id:
#         try:
#             old_product = Product.objects.get(id=instance.id)
#             if old_product.product_image != instance.product_image and old_product.product_image.name != 'default.jpg':
#                 default_storage.delete(old_product.product_image.name)
#         except Product.DoesNotExist:
#             pass

# @receiver(pre_delete, sender=Product)
# def delete_product_media(sender, instance, **kwargs):
#     # Delete the associated media file
#     if instance.product_image:
#         default_storage.delete(instance.product_image.path)

# from django.db.models.signals import pre_delete, pre_save
# from django.dispatch import receiver
# import cloudinary
# import cloudinary.uploader

# from store.models import Product

# @receiver(pre_save, sender=Product)
# def delete_old_product_image(sender, instance, **kwargs):
#     if instance.id:
#         try:
#             old_product = Product.objects.get(id=instance.id)
#             if old_product.product_image != instance.product_image and old_product.product_image.name != 'default.jpg':
#                 cloudinary.uploader.destroy(old_product.product_image.name)
#         except Product.DoesNotExist:
#             pass

# @receiver(pre_delete, sender=Product)
# def delete_product_media(sender, instance, **kwargs):
#     # Delete the associated media file
#     if instance.product_image:
#         cloudinary.uploader.destroy(instance.product_image.name)
