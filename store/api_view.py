from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from store.models import Product, Category
from store.serializers import ProductSerializer
from django.middleware.csrf import get_token
from django.http import JsonResponse
from faker import Faker


class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    filter_fields = ('id',)
    search_fields = ('name',)

class ReportView(APIView):
    """
    POST and GET method ONLY
    """

    def get(self, request):
        csrf_token = get_token(request)
        return JsonResponse({"csrftoken": csrf_token})

    def post(self, request):
        data = request.data
        self.validate(data)
        category = data.get('category')
        products = data.get('products')
        date = data.get('date')
        category_obj = self.get_category(category)
        response = self.handle_products(products, category_obj, date)
        return Response({"message": response})

    def handle_products(self, products, category_obj, date):
        fake = Faker()
        num_paragraphs = 4
        description = '\n\n'.join(fake.paragraph() for _ in range(num_paragraphs))

        response = []
        for product in products:
            obj, created = Product.objects.update_or_create(
                category=category_obj,
                    product_image= product.get('photo'),
                    description= description,
                    price=product.get('price'),
                    name= product.get('title'),)
            if created:
                response.append(f'{obj.product_image} - created')
                # response.append(f' - created')
            else:
                response.append(f'{obj.name} - updated')
        return response

    def get_category(self, category):
        obj, _ = Category.objects.get_or_create(name=category.title())
        return obj

    def validate(self, data):
        if data.get('category') is None:
            raise exceptions.ValidationError(
                'category is null'
            )
        if data.get('products') is None:
            raise exceptions.ValidationError(
                'products is null'
            )
        if data.get('date') is None:
            raise exceptions.ValidationError(
                'date is null'
            )
