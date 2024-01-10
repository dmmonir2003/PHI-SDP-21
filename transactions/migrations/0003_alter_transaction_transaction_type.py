# Generated by Django 4.2.7 on 2024-01-09 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_alter_transaction_transaction_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.IntegerField(choices=[(1, 'Deposit'), (2, 'Withdraw'), (3, 'Loan'), (4, 'Loan Paid'), (5, 'Money Transfer'), (6, 'Money Receive')], null=True),
        ),
    ]
