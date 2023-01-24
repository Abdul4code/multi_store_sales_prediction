from rest_framework import serializers
from .models import Store

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = [
            'store_id',
            'store_name',
            'product_id',
            'product_name',
            'total_sold',
            'total_available'
        ]