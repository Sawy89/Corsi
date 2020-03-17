from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import UserCreationForm
import json
from .models import *



@login_required
def index(request):
    return render(request, 'index.html')


def signup(request):
    '''
    https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
    https://stackoverflow.com/questions/7910769/extending-usercreationform-to-include-email-first-name-and-last-name
    '''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def menu(request):
    # Add info addition & price
    DishProc = Dish.objects.all()
    for dish in DishProc:
        dish.addition_present = dish.addition.exists()
        dish.addition_list = list(dish.addition.values_list('id','name','price'))

        # add prices (if any, leave empty)
        dish.prices = dict(list(DishPrice.objects.filter(dish=dish.id).all().values_list('dimension','price')))
        dish.prices_id = dict(list(DishPrice.objects.filter(dish=dish.id).all().values_list('dimension','id')))
    
    # Add info small/large or normal
    DishCatProc = DishCategory.objects.all()
    for dishcat in DishCatProc:
        list_dim = list(DishPrice.objects.filter(dish__category=dishcat.id).values_list('dimension', flat=True).distinct())
        dishcat.available_dimension = list_dim

    return render(request, 'orders/menu.html', {"DishCategory": DishCatProc,
                                                "Dish": DishProc,
                                                "Toppings": Topping.objects.all()})


@login_required
def shopping_cart(request):
    '''
    Page with the shopping cart
    '''
    # Get cart item
    form_input = request.POST['cart']
    form_input_json = json.loads(form_input)
    cart_items = form_input_json['cart']

    # Process prices
    cart_processed = []
    total = 0
    for item in cart_items:
        # Get data
        dish = DishPrice.objects.filter(id=item['priceId']).first()
        topping = Topping.objects.filter(id__in=item['topping']).all()
        addition = Addition.objects.filter(id__in=item['addition']).all()
        add_str = ', '.join([str(i) for i in topping])
        if add_str != '' and addition:
            add_str += ' - '
        if addition:
            add_str = "Extra: " + (', '.join([str(i.name) for i in addition]))
        # Total price
        total_price = dish.price
        for i in addition:
            total_price += i.price
        
        dish_processed = {"id": item['id'],
                            "dish": str(dish.dish)+" ["+dish.dimension+"]",
                            "add": add_str,
                            "price": total_price}
        
        cart_processed.append(dish_processed)
        total += total_price
        
    return render(request, 'orders/cart.html', {'cart': cart_processed, 'total': total})


