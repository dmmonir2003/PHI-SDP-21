from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Transaction

class TransactionForm(forms.ModelForm):
     class Meta:
          model=Transaction
          fields=['amount','transaction_type']

     def __init__(self,*args, **kwargs ):
          self.account=kwargs.pop('account')
          super.__init__(*args, **kwargs)
          self.fields['transaction_type'].disabled=True
          self.fields['transaction_type'].widget=forms.HiddenInput()
    
     def save(self, commit=True):
          self.instance.account=self.account
          self.instance.balance_after_transaction=self.account.balance
          return super().save()
          
class DepositForm(TransactionForm):
     def clean_amount(self):
          min_deposit_amount=100
          amount=self.cleaned_data.get('amount')
          if amount<min_deposit_amount:
               raise forms.ValidationError(
                    f'tou need to deposit at least {min_deposit_amount} Taka'
               )
          return amount
     
class WithdrawForm(TransactionForm):
     def clean_amount(self):
          account=self.account
          min_withdraw_amount=500
          max_withdraw_amount=50000
          balance=account.balance
          amount=self.cleaned_data.get('amount')
          if amount<min_withdraw_amount:
               raise forms.ValidationError(
                    f'You can withdraw at least {min_withdraw_amount}  Taka'
               )
          if amount>max_withdraw_amount:
               raise forms.ValidationError(
                    f'You can withdraw at most {max_withdraw_amount} Taka'
               )
          if amount>balance:
               raise forms.ValidationError(
                    f' You have {balance} Taka in your account '
                    'You Can not withdraw more then your account current balance'
               )
          return amount
     
class LoanRequestForm(TransactionForm):
     def clean_amount(self):
          amount=self.cleaned_data.get('amount')

          return amount