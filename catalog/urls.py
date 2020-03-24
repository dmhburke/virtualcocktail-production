from django.urls import path
from . import views

urlpatterns = [
    # LANDING PAGE - contains list of businesses
    path('', views.businesslist, name='businesslist'),
    # PAYMENT PAGE - handles amounts and Venmo integration
    path('setcocktails/<business_name>', views.setcocktails, name='setcocktails'),
    # CONFIRMATION PAGE - confirms amount and enables social sharing
    path('confirmation', views.confirmation, name='confirmation'),
    # SUBMIT BUSINESS - form to receive new business submissions
    path('submitbusiness', views.submitbusiness, name='submitbusiness'),

]
