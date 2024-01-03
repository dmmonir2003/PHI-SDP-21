from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction
from .constans import DEPOSIT,WITHDRAWAL,LOAN,LOAN_PAID
from .forms import DepositForm,WithdrawForm,LoanRequestForm
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.


class TransactionCreateViewMixin(LoginRequiredMixin,CreateView):
    template_name=''
    model =Transaction
    title=''
    success_url=''
    

    def get_form_kwargs(self):
        kwargs= super().get_form_kwargs()
        kwargs.update({
            'account':self.request.user.account

        })
        return kwargs
    
    def get_context_data(self, **kwargs) :
        context= super().get_context_data(**kwargs)
        context.update({
            'title':self.title
        })
        return context
    

class DepositView(TransactionCreateViewMixin):
    form_class=DepositForm
    title='Deposit'

    def get_initial(self):
        initial={'transaction_type':DEPOSIT}
        return initial
    def form_valid(self, form):
        amount=form.cleaned_data.get('amount')
        account=self.request.user.account
        account.balance+=amount
        account.save(
            update_fields=['balance']
        )
        messages.success(self.request,f'Your amount {amount} add to your account ')

        return super().form_valid(form)
class WithdrawView(TransactionCreateViewMixin):
    form_class=WithdrawForm
    title='Withdraw'

    def get_initial(self):
        initial={'transaction_type':WITHDRAWAL}
        return initial
    def form_valid(self, form):
        amount=form.cleaned_data.get('amount')
        account=self.request.user.account
        account.balance-=amount
        account.save(
            update_fields=['balance']
        )
        messages.success(self.request,f'Your amount {amount} withdraw to your account ')

        return super().form_valid(form)
class LoanRequestView(TransactionCreateViewMixin):
    form_class=LoanRequestForm
    title='LoanRequest'

    def get_initial(self):
        initial={'transaction_type':LOAN}
        return initial
    def form_valid(self, form):
        amount=form.cleaned_data.get('amount')
        current_loan_count=Transaction.objects.filter(account=self.request.user.account,transaction_type=LOAN,loan_approve=True).count()
        if current_loan_count>=3:
            return HttpResponse('Your loan limits already crossed ')
        
        messages.success(self.request,f'Your amount {amount} Loan request send  to admin successfully  ')

        return super().form_valid(form)
    