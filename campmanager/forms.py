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

class MyProfileForm(forms.Form):
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    phone = forms.CharField(max_length=30)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(MyProfileForm, self).__init__(*args, **kwargs)

    def clean(self):
        cd = self.cleaned_data
        if self.user.username != self.cleaned_data.get('username') and User.objects.filter(username=self.cleaned_data['username']).exists():
            self.add_error('username', "That username already exists.  Choose another.")

                    #user.username = form.cleaned_data.get('username')
                #    user.first_name = form.cleaned_data.get('first_name')
                    #user.last_name = form.cleaned_data.get('last_name')
                    #user.email = form.cleaned_data.get('email')

        #i#f User.objects.filter(username=self.cleaned_data['username']).exists():
            #self.add_error('username', "That username already exists.  Choose another.")
        #if User.objects.filter(email=self.cleaned_data['email']).exists():
            #self.add_error('email', "That email already has an account associated with it.")
        return cd
