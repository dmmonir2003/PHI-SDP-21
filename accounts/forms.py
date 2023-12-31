
from django.contrib.auth.forms import UserCreationForm 
from django import forms
from .constants import ACCOUNT_TYPE,GENDER
from django.contrib.auth.models import User
from .models import UserBankAccount,UserAddress



class UserForm(UserCreationForm):
    account_type=forms.ChoiceField(choices=ACCOUNT_TYPE)
    birth_date=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender=forms.ChoiceField(choices=GENDER)
    street_address=forms.CharField(max_length=100)
    city=forms.CharField(max_length=100)
    postal_code=forms.IntegerField()
    country=forms.CharField(max_length=100)

    class Meta:
        model=User
        fields=['username','email','password1','password2','first_name','last_name','account_type','birth_date','gender','street_address','city','postal_code','country']

    def save (self, commit= True) :
        our_user= super().save(commit=False)
        if commit==True:
            our_user.save()
            account_type=self.cleaned_data.get('account_type')
            birth_date=self.cleaned_data.get('birth_date')
            gender=self.cleaned_data.get('gender')
            street_address=self.cleaned_data.get('street_address')
            city=self.cleaned_data.get('city')
            postal_code=self.cleaned_data.get('postal_code')
            country=self.cleaned_data.get('country')

            UserAddress.objects.create(
            user=our_user,
            street_address=street_address,
            city=city,
            postal_code=postal_code,
            country=country
            )

            UserBankAccount.objects.create(
                user=our_user,
                account_type=account_type,
                gender=gender,
                birth_date=birth_date,
                # ganared account no hendel
                account_no=100000+our_user.id
            )

        return our_user
    
    # style add from bacend
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':(
                    'appearance-none block w-full bg-gray-200 ' 
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
