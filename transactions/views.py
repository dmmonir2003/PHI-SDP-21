
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import CreateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction
from .constans import DEPOSIT,WITHDRAWAL,LOAN,LOAN_PAID
from .forms import DepositForm,WithdrawForm,LoanRequestForm
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Sum
from django.views import View
from django.urls import reverse_lazy

# Create your views here.


class TransactionCreateViewMixin(LoginRequiredMixin,CreateView):
    template_name='transaction/transaction_form.html'
    model =Transaction
    title=''
    success_url=reverse_lazy('transaction_report')
    

    def get_form_kwargs(self):
        kwargs= super().get_form_kwargs()
        kwargs.update({
            'account':self.request.user.account

        })
        return kwargs
    
    def get_context_data(self, **kwargs):
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
    title='Loan Request'

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
    


class TransactionReportView(LoginRequiredMixin,ListView):
       template_name='transaction/transaction_report.html'
       model=Transaction
       balance=0


       def get_queryset(self):
           queryset= super().get_queryset().filter(
               account=self.request.user.account
           )

           start_date_str=self.request.GET.get('start_date')
           end_date_str=self.request.GET.get('end_date')

           if start_date_str and end_date_str:
               
               start_date=datetime.strptime(start_date_str,'%Y-%m-%d').date()
               end_date=datetime.strptime(end_date_str,'%Y-%m-%d').date()


               queryset=queryset.filter(timestamp__date__gte=start_date,timestamp__date__lte=end_date)

               self.balance=Transaction.objects.filter(timestamp__date__gte=start_date,timestamp__date__lte=end_date).aggregate(Sum('amount'))['amount__sum']

           else:
               self.balance=self.request.user.account.balance

           return queryset
       def get_context_data(self, **kwargs) :
            context= super().get_context_data(**kwargs)
            context.update({
            'account':self.request.user.account
             })
            return context


            
class PayLoanViev(LoginRequiredMixin,View):
        def get(self,request,loan_id):
            loan=get_object_or_404(Transaction,id=loan_id)

            if loan.loan_approve:
                user_account=loan.account
                if loan.amount<user_account.balance:
                    user_account.balance-=loan.amount
                    loan.balance_after_transaction=user_account.balance
                    user_account.save()
                    loan.transaction_type=LOAN_PAID
                    loan.save()
                    return redirect('loan_pay')
                else:
                    messages.error(self.request,'loan amount is grater then your current balance ')
                    return redirect('loan_pay')
                


class LoanListView(LoginRequiredMixin,ListView):
    model=Transaction
    template_name='transaction/loan_request.html'
    context_object_name='loans'

    def get_queryset(self):
        user_account=self.request.user.account
        queryset=Transaction.objects.filter(account=user_account,transaction_type=LOAN)
        return queryset
    