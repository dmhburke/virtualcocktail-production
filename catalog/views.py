#Import libraries and dependencies here
from django.shortcuts import render, redirect
from django.db.models import Q

#Import models here
from catalog.models import masterRecord, businessRecord, transactionRecord, addBusiness

#Import forms here
from catalog.forms import BusinessSearchForm, BusinessSearchForm, AddBusinessForm

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

    context = {
    'form': form,
    'business_list': business_list,
    }

    return render(request, 'businesslist.html', context=context)

# ===SET COCKTAIL NUMBERS AND SEND TO VENMO===
def setcocktails(request, business_name):

    business_name = businessRecord.objects.get(business_name=business_name)

    business_image = business_name.background_image

    if request.method =='POST':
         form = OrderForm(request.POST)
         if form.is_valid():
            post = form.save(commit=False)
            post.business_name = business_name
            post.number_input = post.number_input
            post.amount = post.number_input * 15
            post.save()
            return redirect('confirmation')

    else:
          form = OrderForm()

    request.session['business_name'] = business_name.business_name

    context = {
    'business_name': business_name,
    'business_image': business_image,
    'form': form,
    }

    return render(request, 'setcocktails.html', context=context)

#=== CONFIRM PAYMENT AND ENABLE SOCIAL===
def confirmation(request):
    #== import payment library from braintree ==
    import braintree

    #== create oayment gateway object using braintree account keys ==
    gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="snk9pzv46hv7tkdb",
        public_key="p77ssqjzvyv7388r",
        private_key="c564c7143c467ed9548ab23ec4d86208"
        )
    )

    #== create payment using "nonce" (which is the unique payment authorization code) from cront end  ==
    result = gateway.transaction.sale({
        "amount": request.form["quantity"]*15,
        "payment_method_nonce": request.form["nonce"],
        "options": {
          "submit_for_settlement": True,
          "venmo": {
          }
        },
    "device_data": request.form["device_data"]
    })

    business_name = request.session['business_name']
    number_output = transactionRecord.objects.latest('number_input').number_input

    context = {
    'business_name': business_name,
    'number_output': number_output,
    }

    return render(request, 'confirmation.html', context=context)

# ===XXXX===
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
