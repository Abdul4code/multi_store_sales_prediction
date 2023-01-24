from django.db import models

# Create your models here.

class Store(models.Model):
    store_id = models.IntegerField()
    store_name = models.CharField(max_length=200)
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=200)
    total_sold = models.IntegerField()
    total_available = models.IntegerField()

    def __str__(self):
        return "{} - {}".format(self.store_name, self.product_name)
