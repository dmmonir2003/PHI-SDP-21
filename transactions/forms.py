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
          
