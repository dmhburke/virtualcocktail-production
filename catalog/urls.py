from django.urls import path
from . import views

urlpatterns = [
    # LANDING PAGE - contains list of businesses
    path('', views.businesslist, name='businesslist.html'),
    # PAYMENT PAGE - handles amounts and Venmo integration
    path('setcocktails', views.setcocktails, name='setcocktails.html'),
    # CONFIRMATION PAGE - confirms amount and enables social sharing
    path('confirmation', views.confirmation, name='confirmation.html'),
    # SUBMIT BUSINESS - form to receive new business submissions
    path('submitbusiness', views.submitbusiness, name='submitbusiness.html'),

]
