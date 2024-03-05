from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from questAI.models import UserProfile, Products
from django.contrib.auth.models import User
import re


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),
                               required=True,
                               validators=[MinLengthValidator(6)],
                               error_messages={'required': 'Password is required.',
                                               'min_length': 'Password must be at least 6 characters long.'
                                               })
    username = forms.CharField(required=True,
                               error_messages={'required': 'Username is required.'})
    email = forms.EmailField(required=True,
                             error_messages={'required': 'Email is required.'})
    first_name = forms.CharField(required=True,
                                 error_messages={'required': 'First name is required.'})
    last_name = forms.CharField(required=True,
                                error_messages={'required': 'Last name is required.'})
    class Meta:
        model = User
        fields = ('username', 'email','password','first_name','last_name')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)  # Correctly call the parent's __init__
        self.fields['username'].initial = ''  # Set the initial value for username
        self.fields['password'].initial = ''  # Set the initial value for password
        # Set custom help text for username field
        self.fields['username'].help_text = 'Letters, digits and @/./+/-/_ only.'

    def clean_username(self):
        username = self.cleaned_data['username']
        # Check if any other user besides the current user uses this username
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not re.match("^[a-zA-Z]+$", first_name):
            raise ValidationError("First name must only contain letters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not re.match("^[a-zA-Z]+$", last_name):
            raise ValidationError("Last name must only contain letters.")
        return last_name


class UserProfileForm(forms.ModelForm):
    address = forms.CharField(required=True,
                              error_messages={'required': 'Address is required.'})
    postcode = forms.CharField(required=True,
                               error_messages={'required': 'Postcode is required.'})
    class Meta:
        model = UserProfile
        fields = ('address','postcode',)

    def clean_postcode(self):
        postcode = self.cleaned_data['postcode']
        postcode_regex = re.compile(r'^[A-Z]{1,2}\d{1,2} \d[A-Z]{2}$', re.IGNORECASE)
        if not postcode_regex.match(postcode):
            raise forms.ValidationError('Postcode must be in the format of G11 6EQ.')
        return postcode.upper()

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_username(self):
        username = self.cleaned_data['username']
        # Check if any other user besides the current user uses this username
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not re.match("^[a-zA-Z]+$", first_name):
            raise ValidationError("First name must only contain letters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not re.match("^[a-zA-Z]+$", last_name):
            raise ValidationError("Last name must only contain letters.")
        return last_name

class ProductForm(forms.ModelForm):
    # image_path = forms.CharField(required=False)
    class Meta:
        model = Products
        fields = ['productId', 'productName', 'productDescription', 'price', 'category', 'image']

    # def __init__(self, *args, **kwargs):
    #     super(ProductForm, self).__init__(*args, **kwargs)
    #     self.fields['productId'].disabled = True
