from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# CREATE MODELS HERE

class addBusiness(models.Model):
    business_name = models.CharField(max_length=100, blank=True, null=True)
    is_yours = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    instagram_handle = models.CharField(max_length=50, blank=True, null=True)
    email_address = models.CharField(max_length=50, blank=True, null=True)

class businessRecord(models.Model):
    business_name = models.CharField(max_length=50, blank=True, null=True)
    background_image = models.ImageField(upload_to='UploadImage', blank=True, null=True)
    bank_details = models.CharField(max_length=100, blank=True, null=True)
    contact_email = models.CharField(max_length=50, blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.business_name

class transactionRecord(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    business_name = models.ForeignKey('businessRecord', on_delete=models.CASCADE, blank=True, null=True)
    number_input = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

class masterRecord(models.Model):
    business_name = models.ForeignKey('businessRecord', on_delete=models.CASCADE, blank=True, null=True)
    total_number = models.IntegerField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

@receiver (post_save, sender=businessRecord)
def add_business(sender, instance, **kwargs):

    masterRecord.objects.update_or_create(
    business_name=instance,
    defaults = {
    'total_number': 0,
    'total_amount': 0,
    })

@receiver (post_save, sender=transactionRecord)
def add_total(sender, instance, **kwargs):

    # Increment transaction number and amount into the master totals
    old_number = masterRecord.objects.get(business_name=instance.business_name).total_number
    instance_number = instance.number_input
    old_amount = masterRecord.objects.get(business_name=instance.business_name).total_amount
    instance_amount = instance.amount

    new_number = old_number + instance_number
    new_amount = old_amount + instance_amount

    masterRecord.objects.update_or_create(
    business_name=instance.business_name,
    defaults = {
    'total_number': new_number,
    'total_amount': new_amount,
    })
