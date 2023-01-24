from django.contrib import admin
from django.urls import path

from . views import ProductsList
from .views import product_detail, product_update, predict

urlpatterns = [
    path('products', ProductsList.as_view()),
    path('detail/<int:store_id>/<int:product_id>', product_detail),
    path('update', product_update),
    path('predict', predict)
]
