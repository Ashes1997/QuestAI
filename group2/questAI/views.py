from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_POST

from questAI.forms import UserForm, UserProfileForm, UserEditForm, ProductForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from questAI.models import UserProfile, Products, Baskets
from django.contrib import messages


def index(request):
    return render(request, 'questAI/index.html')

@login_required
def home(request):
    products = Products.objects.all()
    return render(request, 'questAI/home.html', {'products': products})


def register(request):
    registered = False#Identifies whether the user has successfully registered
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)#Hash passwords to convert plain text into a secure form
            user.save()
            profile = profile_form.save(commit=False)#Save the database without submitting it, used to associate users with additional information
            profile.user = user#Establish an association between user and profile
            # if 'picture' in request.FILES:
            #     profile.picture = request.FILES['picture']
            profile.save()
            registered = True
            return redirect(reverse('questAI:login'))
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,
              'questAI/register.html',
              context = {'user_form':user_form,
                         'profile_form':profile_form,
                         'registered':registered})


def user_login(request):
    if request.method == 'POST':#POST request is used to submit form data
        username = request.POST.get('username')#Extract username and password from request
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)#This function uses the provided username and password for user authentication. If successful, it returns the user object. If it fails, it returns None.
        if user:
            if user.is_active:#Check whether the user account is active (used for administrators to temporarily deactivate the account)
                login(request,user)#Mark user as logged in
                if user.is_staff == True:
                    return redirect(reverse('questAI:manage_home'))
                else:
                    return redirect(reverse('questAI:home'))#Redirect to website homepage
            else:
                return HttpResponse("Your questAI account is disabled.")
        else:
            print(f"Invalid login details:{username},{password}")
            context={'error_message':"Invalid login details supplied."}
            return render(request,'questAI/login.html',context)
    else:
        return render(request,'questAI/login.html')
@login_required#Restrict access permissions. This view function can only be accessed when the user is logged in. If a user who is not logged in tries to access this view, the user will be automatically redirected to the login page.
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('questAI:login'))

@login_required
def profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    return render(request,'questAI/profile.html',{'user':request.user,'profile':user_profile})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST,instance=request.user)
        profile_form = UserProfileForm(request.POST,instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(reverse('questAI:profile'))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'questAI/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():#Verify that the old password entered by the user is correct，and whether the new password meets the requirements
            user = form.save()
            update_session_auth_hash(request, user)#Ensure users are not logged out after changing their password
            messages.success(request, 'Your password was successfully updated!')
            return redirect(reverse('questAI:profile'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'questAI/change_password.html', {
        'form': form
    })
def manage_home(request):
    products = Products.objects.all()
    return render(request, 'questAI/manage_home.html', {'products': products})

def edit_product(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect(reverse('questAI:manage_home'))
    else:
        form = ProductForm(instance=product)
    return render(request, 'questAI/edit_product.html', {'form': form})

@require_POST
@login_required
def delete_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Products, pk=product_id)
        product.delete()
        return HttpResponseRedirect(reverse('questAI:manage_home'))
    else:
        return HttpResponseRedirect(reverse('questAI:manage_home'))

def add(request):
    return render(request, 'questAI/add.html')


@login_required
def basket(request):
    if not request.user.is_authenticated:
        return render(request, 'questAI/login.html')
    basket_items = Baskets.objects.filter(username=request.user)
    
    total_price = 0
    for item in basket_items:
        item.total_price = item.price * item.quantity
        total_price += item.total_price
    context = {
        'basket_items': basket_items,
        'total_price': total_price
    }
    return render(request, 'questAI/basket.html', context)

def topup(request):
    return HttpResponse("Test for Top Up Page")

def checkout(request):
    return HttpResponse("Test for Checkout Page")

def add_to_basket(request, product_id):
    print("Adding to basket...")
    if request.method == "POST":
        product = get_object_or_404(Products, pk=product_id)
        user = request.user
        basket_item, created = Baskets.objects.get_or_create(
            username=user, productId=product,
            defaults={'price': product.price, 'quantity': 1})
        if not created:
            basket_item.quantity += 1
            basket_item.save()
        return JsonResponse({'status': 'success', 'message': 'Product added to basket'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    

@login_required
@require_POST
def update_basket(request):
    item_id = request.POST.get('item_id')
    action = request.POST.get('action')
    user = request.user
    
    basket_item = get_object_or_404(Baskets, basketId=item_id, username=user)
    
    if action == "increase":
        basket_item.quantity += 1
    elif action == "decrease":
        # Check if the quantity is greater than 1 before decrementing
        if basket_item.quantity > 1:
            basket_item.quantity -= 1
        else:
            # If quantity will be less than 1, remove the item from the basket
            basket_item.delete()
            return JsonResponse({'status': 'success', 'message': 'Item removed from basket'})

    basket_item.save()

    return JsonResponse({'status': 'success', 'message': 'Basket updated successfully'})

