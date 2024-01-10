from django.urls import path
from .views import DepositView,WithdrawView,LoanListView,LoanRequestView,PayLoanViev,TransactionReportView,MoneyTransferView
urlpatterns = [
    path('deposit/',DepositView.as_view(),name='deposit'),
    path('withdraw/',WithdrawView.as_view(),name='withdraw'),
    path('transaction_report/',TransactionReportView.as_view(),name='transaction_report'),
    path('loan_request/',LoanRequestView.as_view(),name='loan_request'),
    path('loans/',LoanListView.as_view(),name='loans'),
    path('loan/<int:loan_id>/',PayLoanViev.as_view(),name='loan_pay'),
    path('money_transfer/',MoneyTransferView.as_view(),name='money_transfer'),
    
   
]