from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import UserCreationForm
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
        # add prices (if any, leave empty)
        dish.prices = dict(list(DishPrice.objects.filter(dish=dish.id).all().values_list('dimension','price')))
        for i in DishPrice.DimensionType.choices:
            if i[0] not in dish.prices.keys():
                dish.prices[i[0]] = ' - '
    
    # Add info small/large or normal
    DishCatProc = DishCategory.objects.all()
    for dishcat in DishCatProc:
        list_dim = list(DishPrice.objects.filter(dish__category=dishcat.id).values_list('dimension', flat=True).distinct())
        dishcat.available_dimension = list_dim


    return render(request, 'orders/menu.html', {"DishCategory": DishCatProc,
                                                "Dish": DishProc,
                                                "Addition": Addition.objects.all()})


def get_toppings(request):
    '''
    Get the toppings for pizzas!
    '''

