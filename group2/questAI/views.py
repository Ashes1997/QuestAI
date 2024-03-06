from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render
from django.http import HttpResponse
from questAI.forms import UserForm, UserProfileForm, UserEditForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from questAI.models import UserProfile, Products
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
                    return redirect(reverse('questAI:manage'))
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
def manage(request):
    return render(request, 'questAI/managebase.html')
def add(request):
    return render(request, 'questAI/add.html')
def basket(request):
    return HttpResponse("Test for Basket Page")

def topup(request):
    return HttpResponse("Test for Top Up Page")

def checkout(request):
    return HttpResponse("Test for Checkout Page")

# Test page for google maps api
def enter_locations(request):
    if request.method == "POST":
        # Assuming you have a form to capture 'start_location' and 'end_locations' (as a list)
        start_location = request.POST.get('start_location')
        end_locations = request.POST.getlist('end_locations[]')  # Adjust based on your form
        # Redirect to the map view with the locations as arguments
        return render(request, "questAI/display_map.html", {
            "start_location": start_location,
            "end_locations": end_locations,
            "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY
        })
    return render(request, "questAI/enter_locations.html")

