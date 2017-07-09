from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from thisaintjack import site_config


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    magicword = forms.CharField(max_length=30 )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'magicword')

    def clean(self):
        cd = self.cleaned_data
        if cd.get('magicword') != site_config.MAGICWORD:
            self.add_error('magicword', "worng word !")
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            self.add_error('username', "That username already exists.  Choose another.")
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            self.add_error('email', "That email already has an account associated with it.")
        return cd
