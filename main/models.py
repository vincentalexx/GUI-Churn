from django.db import models

# Create your models here.
class Customer(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    is_tv_subscriber = models.BooleanField(default=False)
    is_movie_package_subscriber = models.BooleanField(default=False)
    subscription_age = models.FloatField()
    bill_avg = models.FloatField(default=0)
    reamining_contract = models.FloatField(default=0)
    download_avg = models.FloatField(default=0)
    upload_avg = models.FloatField(default=0)
    download_over_limit = models.FloatField(default=0)
    is_contract = models.BooleanField(default=False)
    class Meta:
        db_table = 'Customers'