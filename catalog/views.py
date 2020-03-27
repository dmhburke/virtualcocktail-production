#Import libraries and dependencies here
from django.shortcuts import render, redirect
from django.db.models import Q
#email libraries
from django.core.mail import send_mail
from django.conf import settings

#Import models here
from catalog.models import masterRecord, businessRecord, transactionRecord, addBusiness

#Import forms here
from catalog.forms import BusinessSearchForm, BusinessSearchForm, AddBusinessForm, OrderForm

# Create your views here.

# ===LANDING PAGE===
def businesslist(request):

    business_select = []

    if request.method =='POST':
         form = BusinessSearchForm(request.POST)
         if form.is_valid():
             business_select = form.search_input(request)

    else:
          form = BusinessSearchForm()

    if len(business_select) == 0:
        business_list = masterRecord.objects.all()
    else:
        business_list = masterRecord.objects.filter(
        Q(business_name__business_name__contains=business_select) | Q(business_name__postcode__contains=business_select) #NOTE: NEED TO UPDATE MODEL TO INCLUDE POSTCODE
        ).order_by('-total_amount')

    # business_pic = addBusiness.objects.get(id=1).background_image
    # print("<<PIC IS:>>")
    # print(business_pic)

    context = {
    'form': form,
    'business_list': business_list,
    }

    return render(request, 'businesslist.html', context=context)

# ===SET COCKTAIL NUMBERS AND SEND TO VENMO===
def setcocktails(request, business_name):

    #== import payment library from braintree ==
    import braintree

    #== create payment gateway object using braintree account keys ==
    gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="snk9pzv46hv7tkdb",
        public_key="p77ssqjzvyv7388r",
        private_key="c564c7143c467ed9548ab23ec4d86208"
        )
    )

    #== Create Braintree customer token ==
    client_token = gateway.client_token.generate({
    })

    business_instance = businessRecord.objects.get(business_name=business_name)
    business_ref = businessRecord.objects.get(business_name=business_name)

    # CREATE FORM
    if request.method =='POST':
        form = OrderForm(request.POST)

        #== set key form details
        post = form.save(commit=False)
        post.business_name = business_instance
        post.number_input = post.number_input
        post.amount = int(post.number_input) * 15

        #== pull Braintree variables directly from form ==
        nonce = request.POST.get('nonce')
        device_data = request.POST.get('device_data')
        email_details = request.POST.get('add-friends-form')
        full_payload = request.POST.get('full_payload')

        #== create payment using "nonce" (which is the unique payment authorization code) from cront end  ==
        result = gateway.transaction.sale({
            "amount": str(post.amount),
            "payment_method_nonce": nonce,
            "options": {
                "submit_for_settlement": True,
                # "venmo": {"profile_id": 'sandbox_s9zvtq2d_snk9pzv46hv7tkdb'
                # }
            },
            "device_data": device_data,
            "custom_fields": {
                "restaurant_name": str(business_name),
            }
        })
        #== Check payment was successful
        if result.is_success:
            print("SUCCESS")
            cardholder_name = result.transaction.credit_card_details.cardholder_name
            if cardholder_name == None:
                payer_name = "A secret admirer"
            else:
                payer_name = cardholder_name
            ## Create email list
            email_list = email_details.split(",")
            # print(email_list)
            ## send email to email list
            send_mail(
                'Your Virtual Cocktail is Served!',
                'Great news! {} has just bought you a virtual cocktail from {} on The Virtual Cocktail.\n\nThe Virtual Cocktail is a donation platform supporting local businesses through COVID-19.\n\nFind a business to support and order the next round at www.virtualcocktail.org.\n\nStay safe, support local businesses, and we hope to see you soon!\n\nThe Virtual Cocktail Team'.format(payer_name, business_instance),
                'virtualcocktailorg@gmail.com',
                email_list,
                fail_silently=False,
            )
            post.save()
            return redirect('confirmation')

        else:
            print('failure')

    else:
        form = OrderForm()


    #== Save key details as session variables
    request.session['business_name'] = business_name

    context = {
    'form': form,
    'business_name': business_name,
    'business_ref': business_ref,
    'client_token': client_token,
    }

    return render(request, 'setcocktails.html', context=context)

#=== CONFIRM PAYMENT AND ENABLE SOCIAL===
def confirmation(request):

    # define key variables
    business_name = request.session['business_name']
    number_input = transactionRecord.objects.last().number_input
    business_ref = businessRecord.objects.get(business_name=business_name)

    context = {
    'business_name': business_name,
    'number_input': number_input,
    'business_ref': business_ref,
    }

    return render(request, 'confirmation.html', context=context)

# === FORM FOR USERS TO ADD OR REQUEST A NEW BUSINESS ===
def submitbusiness(request):

    if request.method =='POST':
         form = AddBusinessForm(request.POST)
         if form.is_valid():
            post = form.save(commit=False)
            post.save()
            request.session['add_business_name'] = post.business_name
            request.session['add_business_owner'] = post.is_yours
            return redirect('submitbusinessconfirm') # change to confirmation page
    else:
          form = AddBusinessForm()

    context = {
    'form': form,
    }

    return render(request, 'submitbusiness.html', context=context)

#== CONFIRMATION PAGE FOLLOWING NEW BUSINESS SUBMIT ==
def submitbusinessconfirm(request):

    try:
        add_business_name = request.session['add_business_name']
    except:
        add_business_name = "a new business"

    try:
        add_business_owner = request.session['add_business_owner']
    except:
        add_business_owner = "Unable to get"


    context = {
        'add_business_name': add_business_name,
        'add_business_owner': add_business_owner,
    }

    return render(request, 'submitbusinessconfirm.html', context=context)

def aboutus(request):

    context={}

    return render(request, 'about.html', context=context)
