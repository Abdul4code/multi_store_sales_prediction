from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, UpdateAPIView
from datetime import datetime


from .serializer import StoreSerializer
from .models import Store
from utils.utilities import create_prediction_dataframe, preprocess
from utils.utilities import predict as predict_sales

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
    start_date = datetime.strptime(request.data['start_date'], "%Y-%m-%d")
    period = request.data['period']
    store_id = request.data['store_id']
    product_id = request.data['product_id']

    df = create_prediction_dataframe(start_date, period, store_id, product_id)
    stop_date = df.loc[df.index[-1], 'date']
    df = preprocess(df)
    pred, daily_average = predict_sales(df)

    return Response(
        {
            "prediction": pred,
            "period": period,
            "daily_average": daily_average,
            "start_date": start_date,
            "end_date": stop_date
        }
    )

@api_view(['GET'])
def product_filter(requets, store_id, product_id):
    if(store_id == 0 and product_id == 0):
        print("hurray")
        queryset = Store.objects.all()
    elif store_id == 0:
        queryset = Store.objects.filter(product_id = product_id)
    elif product_id == 0:
        queryset = Store.objects.filter(store_id = store_id)
    else:
        queryset = Store.objects.filter(product_id = product_id).filter(store_id = store_id)

    serializer = StoreSerializer(queryset, many=True)

    return Response(
        serializer.data
    )
