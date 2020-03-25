#import libraries and dependencies here
from django import forms
from catalog.choices import *

# import models for ModelForms
from catalog.models import transactionRecord, addBusiness

class AddBusinessForm(forms.ModelForm):
    business_name = forms.CharField(required=True)
    is_yours = forms.ChoiceField(choices=YES_NO, required=False)
    phone_number = forms.CharField(required=False)
    email_address = forms.CharField(required=False)
    instagram_handle = forms.CharField(required=False)

    class Meta:
        model = addBusiness
        fields = ('business_name', 'is_yours', 'phone_number', 'email_address', 'instagram_handle',)


class OrderForm(forms.ModelForm):
    number_input = forms.IntegerField(label='', required=False, initial=1)

    class Meta:
        model = transactionRecord
        fields = ('number_input',)

class BusinessSearchForm(forms.Form):
    find_business = forms.CharField(required=False)

    def search_input(self,request):
        businessSelect = self.cleaned_data['find_business']
        return businessSelect
