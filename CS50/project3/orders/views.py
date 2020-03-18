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



@login_required
def place_order(request):
    '''
    Page for placing the order
    '''
    try:
        # Get cart item
        form_input = request.POST['cart']
        form_input_json = json.loads(form_input)
        cart_items = form_input_json['cart']
        current_user = request.user

        # New order
        order = Orders(user=current_user)
        order_to_save = []
        data_to_save = []

        # Process prices
        total = 0
        for item in cart_items:
            # Get data
            dish = DishPrice.objects.filter(id=item['priceId']).first()
            topping = Topping.objects.filter(id__in=item['topping']).all()
            addition = Addition.objects.filter(id__in=item['addition']).all()
            
            # Create order data: dish & topping
            order_dish = OrdersDish(order=order, dish_price=dish)
            for topp in topping:
                order_topp = OrdersTopping(order_dish=order_dish, topping=topp)
                data_to_save.append(order_topp)

            # Addition & Total price
            total_price = dish.price
            for addit in addition:
                order_add = OrdersAddition(order_dish=order_dish, addition=addit)
                data_to_save.append(order_add)
                total_price += addit.price
            order_dish.total_price = total_price
            order_to_save.append(order_dish)
            
            total += total_price
        
        order.total_price = total

        # Save all
        order.save()
        for i in order_to_save:
            i.save()
        for i in data_to_save:
            i.save()

        status = {'order_ok': True, 'alert_message': 'OK! Order inserted!'}

    except:
        status = {'order_ok': False, 'alert_message': 'No OK!, there was a problem in your order. Try again later'}

    return render(request, 'index.html', status)


@login_required()
def orders(request):
    current_user = request.user
    orders_completed = Orders.objects.filter(user=current_user, completed=True).all()
    for order in orders_completed:
        order.n_dish = order.countDish()
        dish = OrdersDish.objects.filter(order=order).all()
        order.dishes = []
        for item in dish:
             order.dishes.append({'str_': item.getDishAddTopping(),
                                        'price': item.total_price})
    
    orders_opened = Orders.objects.filter(user=current_user, completed=False).all()
    for order in orders_opened:
        order.n_dish = order.countDish()
        dish = OrdersDish.objects.filter(order=order).all()
        order.dishes = []
        for item in dish:
             order.dishes.append({'str_': item.getDishAddTopping(),
                                        'price': item.total_price})

    return render(request, 'orders/orders.html', {"orders_completed": orders_completed, "orders_opened": orders_opened})