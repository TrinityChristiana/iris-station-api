'''
A django page to handle all product fetch calls

'''
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Product, Customer

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for products

    Arguments:
        serializers
    """
    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='products',
            lookup_field='id'
        )
        fields = ('id', 'title', 'price', 'description', 'quantity', "location", 'created_at', 'image_path', 'product_type_id')
        depth = 1

class Products(ViewSet):

    '''' a class to handle all the products viewset

    Arguments:
        ViewSet '''

    def create(self, request):
        ''' Handle POST operations and returns JSON serialized product instance'''

        newproduct = Product()
        newproduct.title = request.data["title"]
        newproduct.price = request.data["price"]
        newproduct.description = request.data["description"]
        newproduct.quantity = request.data["quantity"]
        newproduct.location = request.data["location"]
        newproduct.image_path = request.data["image_path"]
        newproduct.created_at = request.data["created_at"]
        newcustomer = Customer.objects.get(user = request.auth.user)
        newproduct.customer = newcustomer
        newproduct.save()

        serializer = ProductSerializer(newproduct, context={'request': request})

        return Response(serializer.data)
    
    def list(self, request):
        ''' handles get requests to server and returns a JSON response'''
        
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True, context={"request": request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        pass
    def update(self, request, pk=None): 
        pass

    def destroy(self, request, pk=None):
        pass