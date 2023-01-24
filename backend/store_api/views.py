from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, UpdateAPIView
from calendar import monthrange

from .serializer import StoreSerializer
from .models import Store

# Create your views here.

class ProductsList(ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


@api_view(['GET'])
def product_detail(request, store_id, product_id):
    result = Store.objects.filter(store_id=store_id).filter(product_id=product_id)
    serializer = StoreSerializer(result, many=True)
   
    return Response(
            serializer.data
        
    )

@api_view(['POST'])
def product_update(request):
    store_id = request.data['store_id']
    product_id = request.data['product_id']
    total_sold = request.data['total_sold']
    total_available = request.data['total_available']

    product = Store.objects.filter(store_id=store_id).filter(product_id=product_id)
    product.update(total_sold=total_sold, total_available=total_available)

    result = Store.objects.filter(store_id=store_id).filter(product_id=product_id)
    serializer = StoreSerializer(result, many=True)

    return Response(
        serializer.data
    )

@api_view(['POST'])
def predict(request):
    #period = request.data['period']
    days_in_month = num_days = monthrange(2019, 2)[1] # number of days in the month

    print(days_in_month) 
