import os
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_POST
from questAI.forms import UserForm, UserProfileForm, UserEditForm, ProductForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from questAI.models import UserProfile, Products, Baskets, Comments, Purchase, Reviews
from django.contrib import messages
from chatGPT import quest_create, chatbot
from django.db.models import Count, Q


def index(request):
    return render(request, 'questAI/index.html')

# @login_required
def home(request):
    products = Products.objects.annotate(
        likes_count=Count('reviews', filter=Q(reviews__review_type='like')),
        dislikes_count=Count('reviews', filter=Q(reviews__review_type='dislike')),
    ).all()
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
def user_logout(request):#Safe user logout
    logout(request)
    return redirect(reverse('questAI:login'))


@login_required
def profile(request):#get the specific user and show the profile
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    return render(request,'questAI/profile.html',{'user':request.user,'profile':user_profile})


@login_required
def edit_profile(request):
    if request.method == 'POST':#Obtain user submission request and determine whether the content is valid
        user_form = UserEditForm(request.POST,instance=request.user)
        profile_form = UserProfileForm(request.POST,instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(reverse('questAI:profile'))
    else:#Display of information before request
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
    return render(request, 'questAI/change_password.html', {'form': form})

@login_required
def manage_home(request):#show the product information
    products = Products.objects.all()
    return render(request, 'questAI/manage_home.html', {'products': products})
@login_required
def edit_product(request, product_id):#Obtain product information based on product ID and modify it
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
def delete_product(request, product_id):#Delete items from database
    if request.method == 'POST':
        product = get_object_or_404(Products, pk=product_id)
        if product.image:#Remove images from media files
            image_path = product.image.path
            if os.path.isfile(image_path):
                os.remove(image_path)
        product.delete()
        return HttpResponseRedirect(reverse('questAI:manage_home'))
    else:
        return HttpResponseRedirect(reverse('questAI:manage_home'))

@login_required
def add_product(request):#Complete the new product details in the form and save them to the database
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('questAI:manage_home'))
    else:
        form = ProductForm()
    return render(request, 'questAI/add_product.html',{'form':form})

@login_required
def search_product(request):#Use filters to filter queries and display corresponding products
    query = request.GET.get('query', '')
    if query:
        products = Products.objects.filter(productName__icontains=query)
    else:
        products = Products.objects.all()
    return render(request, 'questAI/search_product.html', {'products': products, 'query': query})

def search_home_product(request):
    query = request.GET.get('query', '')
    if query:
        products = Products.objects.filter(productName__icontains=query)
    else:
        products = Products.objects.all()
    return render(request, 'questAI/search_home_product.html', {'products': products, 'query': query})


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

@login_required
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

def product_detail(request, product_id):
    product = Products.objects.get(productId=product_id)
    comments = Comments.objects.filter(productId=product)
    context = {'product': product, 'comments': comments}
    return render(request, 'questAI/product_detail.html', context)

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

@login_required
def checkout(request):
    basket_items = Baskets.objects.filter(username=request.user)
    products_string = ', '.join([f"{item.productId.productName}" for item in basket_items])
    
    if basket_items.exists():
        for item in basket_items:

            Purchase.objects.create(
                user=request.user,
                product=item.productId,
                quantity=item.quantity,
                purchase_date=timezone.now() 
            )
            
        
        if products_string:  
            quest = quest_create(products_string)
        else:
            quest = "Your basket is empty. Add some products to generate a quest."

        context = {'quest': quest, 'basket_items': basket_items}
        basket_items.delete()  
        request.session.pop("past_messages", None)
        return render(request, 'questAI/checkout.html', context)
    else:
        context = {'message': "Your basket is empty. Add some products to generate a quest."}
        return render(request, 'questAI/checkout.html', context)

def questbot_ask(request):
    if request.method == "POST":
        user_message = request.POST.get("message")
        quest = request.POST.get("quest", "")  
        past_messages = request.session.get("past_messages", [])
        
        reply, updated_past_messages = chatbot(quest, user_message, past_messages)
        
        
        request.session["past_messages"] = updated_past_messages
        
        return JsonResponse({"reply": reply})

    return JsonResponse({"error": "This endpoint only supports POST requests."}, status=405)

@login_required
@require_POST
def like_dislike(request, product_id):
    user = request.user
    product = get_object_or_404(Products, pk=product_id)
    
    # Check if the user has purchased the product
    if not Purchase.objects.filter(user=user, product=product).exists():
        return JsonResponse({'status': 'error', 'message': 'You must purchase the product before reviewing it.'}, status=403)
    

    review_type = 'like' if request.POST.get('like') == 'true' else 'dislike'
    
    # Get or create review, updating if already exists
    review, created = Reviews.objects.get_or_create(
        username=user, 
        productId=product, 
        defaults={'review_type': review_type}
    )
    
    if not created:

        review.review_type = review_type
        review.save()
    

    likes_count = Reviews.objects.filter(productId=product, review_type='like').count()
    dislikes_count = Reviews.objects.filter(productId=product, review_type='dislike').count()
    
    action = "Liked" if review_type == 'like' else "Disliked"
    return JsonResponse({
        'status': 'success', 
        'message': f'Product successfully {action}.',
        'likes': likes_count,  
        'dislikes': dislikes_count  
    })