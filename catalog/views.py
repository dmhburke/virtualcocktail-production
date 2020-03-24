#Import libraries and dependencies here
from django.shortcuts import render, redirect
from django.db.models import Q

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
        Q(business_name__business_name__contains=business_select)
        ).order_by('-total_amount')

    # request.session['business_name'] = business_name

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

    business_instance = businessRecord.objects.get(business_name=business_name)

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

        #== create payment using "nonce" (which is the unique payment authorization code) from cront end  ==
        result = gateway.transaction.sale({
            "amount": str(post.amount),
            "payment_method_nonce": nonce,
            "options": {
                "submit_for_settlement": True,
                "venmo": {"profile_id": 'sandbox_s9zvtq2d_snk9pzv46hv7tkdb'
                }
            },
            "device_data": device_data,
            "custom_fields": {
                "restaurant_name": str(business_name),
            }
        })
        #== Check payment was successful
        if result.is_success:
            print('success')
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
    }

    return render(request, 'setcocktails.html', context=context)

#=== CONFIRM PAYMENT AND ENABLE SOCIAL===
def confirmation(request):

    # define key variables
    business_name = request.session['business_name']
    number_input = transactionRecord.objects.last().number_input

    context = {
    'business_name': business_name,
    'number_input': number_input,
    }

    # # SET business name
    # #business_name = request.session['business_name']
    # business_name = businessRecord.objects.get(business_name="Minetta Tavern")
    # business_name_string = str(business_name)
    #
    # #== import payment library from braintree ==
    # import braintree
    #
    # #== create payment gateway object using braintree account keys ==
    # gateway = braintree.BraintreeGateway(
    # braintree.Configuration(
    #     braintree.Environment.Sandbox,
    #     merchant_id="snk9pzv46hv7tkdb",
    #     public_key="p77ssqjzvyv7388r",
    #     private_key="c564c7143c467ed9548ab23ec4d86208"
    #     )
    # )
    #
    # if request.method =='POST':
    #     #== pulling required variables directly from form request ==
    #     nonce = request.POST.get('nonce')
    #     number_input = request.POST.get('number_input')
    #     amount = int(number_input) * 15
    #     device_data = request.POST.get('device_data')
    #
    #     #== create payment using "nonce" (which is the unique payment authorization code) from cront end  ==
    #     result = gateway.transaction.sale({
    #         "amount": amount,
    #         "payment_method_nonce": nonce,
    #         "options": {
    #             "submit_for_settlement": True,
    #             "venmo": {"profile_id": 'sandbox_s9zvtq2d_snk9pzv46hv7tkdb'
    #             }
    #         },
    #         "device_data": device_data,
    #         "custom_fields": {
    #             "restaurant_name": business_name_string,
    #         }
    #     })
    #
    #     transacted_amount = result.transaction.amount
    #     number_output = transacted_amount / 15
    #
    #     if result.is_success:
    #         print('success')
    #         transactionRecord.objects.create(
    #             business_name=business_name,
    #             number_input=number_output,
    #             amount=transacted_amount
    #         )
    #     else:
    #         print('failure')
    #         # return redirect('failure')
    #
    context = {
    'business_name': business_name,
    'number_input': number_input,

    }

    return render(request, 'confirmation.html', context=context)

# === FORM FOR USERS TO ADD OR REQUEST A NEW BUSINESS ===
def submitbusiness(request):

    if request.method =='POST':
         form = AddBusinessForm(request.POST)
         if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('submitbusiness') # change to confirmation page
    else:
          form = AddBusinessForm()

    context = {
    'form': form,
    }

    return render(request, 'submitbusiness.html', context=context)
