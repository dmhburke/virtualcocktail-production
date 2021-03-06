from django.contrib import admin

# Register your models here.
from catalog.models import businessRecord, transactionRecord, masterRecord, addBusiness

class addBusinessAdmin(admin.ModelAdmin):
     list_display = ('business_name', 'is_yours', 'phone_number', 'email_address', 'instagram_handle',)

# Register the admin class with the associated model
admin.site.register(addBusiness, addBusinessAdmin)

#Define admin class - create business record
class businessRecordAdmin(admin.ModelAdmin):
     list_display = ('business_name',)

# Register the admin class with the associated model
admin.site.register(businessRecord, businessRecordAdmin)

#Define admin class - create business record
class transactionRecordAdmin(admin.ModelAdmin):
     list_display = ('date', 'donor_name', 'business_name', 'email_list', 'number_input', 'amount',)

# Register the admin class with the associated model
admin.site.register(transactionRecord, transactionRecordAdmin)

class masterRecordAdmin(admin.ModelAdmin):
     list_display = ('business_name', 'total_number', 'total_amount',)

# Register the admin class with the associated model
admin.site.register(masterRecord, masterRecordAdmin)
