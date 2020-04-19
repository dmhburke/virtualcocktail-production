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
    # SUBMIT BIZ CONFIRMATION - page to route to after business submitted
    path('submitbusinessconfirm', views.submitbusinessconfirm, name='submitbusinessconfirm'),
    # ABOUT US - menu dropdown page
    path('aboutus', views.aboutus, name='aboutus'),
    # PWA TEST
    path('', views.serviceworker.as_view(), name='sw'),

]
