from django import forms
from django.core.validators import MinLengthValidator

from questAI.models import UserProfile
from django.contrib.auth.models import User


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



class UserProfileForm(forms.ModelForm):
    address = forms.CharField(required=True,
                              error_messages={'required': 'Address is required.'})
    postcode = forms.CharField(required=True,
                               error_messages={'required': 'Postcode is required.'})
    class Meta:
        model = UserProfile
        fields = ('address','postcode',)
