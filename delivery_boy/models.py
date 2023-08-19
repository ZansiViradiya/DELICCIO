from django.db import models
from foodordering import constant


# Create your models here.
class Delivery(models.Model):
    deliver_name = models.CharField(max_length=50)
    is_approved = models.BooleanField(default=False)
    vehicle_type = models.CharField(
        max_length=10, choices=constant.VEHICLE_CHOISES, default="bike"
    )
    vehicle_no = models.CharField(max_length=10, default=None)
    address = models.ForeignKey('core.Address', null=True, blank=True, on_delete=models.SET_NULL)
    contact = models.ForeignKey('core.Contact', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)