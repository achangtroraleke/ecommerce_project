from django.shortcuts import render, redirect
from .models import User, Tag, Item, Cart
from .forms import ItemForm, MyUserCreationForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    all_sales = Item.objects.filter(
        Q(seller__email__icontains=q) |
        Q(name__icontains=q)|
        Q(description__icontains=q)
    )
    promoted_tag = Tag.objects.get(name='promoted')
    promoted_tag2 = Tag.objects.get(name='promoted2')
    promoted_items = Item.objects.filter(tags=promoted_tag)
    promoted_items2 = Item.objects.filter(tags=promoted_tag2)
   

    context = {'saleitems':promoted_items, 'saleitems2':promoted_items2, 'all_sales':all_sales}
    return render(request, 'base/home.html', context)

@login_required(login_url='login')
def createSale(request):
    form = ItemForm()
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            Item.objects.create(
                seller = request.user,
                picture = form.cleaned_data['picture'],
                name = form.cleaned_data['name'],
                price = form.cleaned_data['price'],
                description = form.cleaned_data['description']
            )
            return redirect('home')
    context ={'form':form}
    return render(request, 'base/create-sale.html', context)

def itemPage(request, pk):
    selected_item = Item.objects.get(id=pk)

    if request.user.is_authenticated:
        guest_cart = Cart.objects.get(user = request.user).items.all()
    else:
        if 'cart_list' not in request.session:
            request.session['cart_list'] = []
            guest_cart=[]
            print('this')
        else:
            cart = request.session['cart_list']
            guest_cart = []
            for item in cart:
                item_data = Item.objects.get(id=item)
                guest_cart.append(item_data)
            print('that')
    context = {'selected_item':selected_item, 'cart':guest_cart}
    return render(request, 'base/item-page.html', context)


def addItem(request, pk):
    selected_item = Item.objects.get(id=pk)

    if request.user.is_authenticated:
        user_cart = Cart.objects.get(user = request.user)
        current_cart =user_cart.items
        current_cart.add(selected_item)
        
        
    else:

        if 'cart_list' in request.session:
            print('added')
            request.session['cart_list']+=([str(selected_item.id)])
        
        else:
            print('created')
            request.session['cart_list'] = [str(selected_item.id)]
  
        
    return redirect('home')


def cartPage(request):
    total = 0
    if request.user.is_authenticated:
        guest_cart = Cart.objects.get(user = request.user).items.all()
        for item in guest_cart:
            total += item.price

    else:
        guest_cart = []
    
        if 'cart_list' not in request.session:
            request.session['cart_list'] = []
        else:
            cart = request.session['cart_list']
            for item in cart:
                item_data = Item.objects.get(id=item)
                guest_cart.append(item_data)
                total += item_data.price
    context = {'cart':guest_cart, "cart_total": total}
    return render(request, 'base/cart.html', context)


def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user=User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, username = email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password is incorrect")

    context = {'page':page}
    return render(request, 'base/login_register.html', context)


login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    form = MyUserCreationForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.username= user.username.lower()
            user.save()
            login(request, user)
            Cart.objects.create(
                user = request.user
            )
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/login_register.html', context)


def checkout(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cart.items.all().delete()
        cart.save()

    else:
        request.session['cart_list'] = []

    return redirect('home')