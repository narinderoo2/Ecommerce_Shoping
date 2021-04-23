from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput
from user.models import UserProfile


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name')
        widgets = {
            'username' :TextInput(attrs = {'class': 'input form-control','placeholder':'user name',}),
            'email' : EmailInput(attrs = {'class': 'input form-control','placeholder':'email'}),
            'first_name' : TextInput(attrs = {'class': 'input form-control','placeholder':'first_name'}),
            'last_name' : TextInput(attrs = {'class': 'input form-control','placeholder':'last_name'}),
        }


CITY = [
    ('Chandigrah','Chandigrah'),
    ('Delhi','Delhi'),
    ('Mumbai','Mumbai'),
]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone','address','city','country','image')
        widgets = {
            'phone' : TextInput(attrs = {'class': 'input form-control','placeholder':'phone'}),
            'address' : TextInput(attrs = {'class': 'input form-control','placeholder':'address'}),
            'city' : Select(attrs = {'class': 'input form-control','placeholder':'city'},choices=CITY),
            'country' : TextInput(attrs = {'class': 'input form-control','placeholder':'country'}),
            'image' : FileInput(attrs = {'class': 'img','placeholder':'image'}),
        }

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length = 30, label='User Name :')
    email = forms.EmailField(max_length=200, label='Email :')
    first_name = forms.CharField(max_length=100,label='First Name :')
    last_name = forms.CharField(max_length=100, label='Last Name :')

    class Meta:
        model = User
        fields = ('username' , 'email', 'first_name','last_name','password1','password2',)

