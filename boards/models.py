from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    message = models.TextField(max_length=4000)
    board = models.ForeignKey(Board, related_name='posts', on_delete='CASCADE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete='CASCADE')
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete='CASCADE')

    def __str__(self):
        return self.message

class Comment(models.Model):
    message = models.TextField(max_length=4000)
    post = models.ForeignKey(Post, related_name='comments', on_delete='CASCADE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='comments', on_delete='CASCADE')
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete='CASCADE')

class Income(models.Model):
    transactionID = models.CharField(max_length=10, unique=True)
    amount = models.FloatField()
    inType = models.CharField(max_length=15)
    payed_to = models.ForeignKey(User, null=False, related_name='incomes', on_delete='CASCADE')
    date_earned = models.DateField()
    year_earned = models.IntegerField()

    def __init__(self, t, a, i, p, y):
        self.transactionID= t
        self.amount = a
        self.inType = i
        self.payed_to = p
        self.year_earned = y

        
class Expense(models.Model):
    transactionID = models.CharField(max_length=10, unique=True)
    amount = models.FloatField()
    exType = models.CharField(max_length=20)
    payed_by = models.ForeignKey(User, null=False, related_name='expenses', on_delete='CASCADE')
    date_spent = models.DateField()
    year_spent = models.IntegerField()

    def __init__(self, t, a, i, p, y):
        self.transactionID= t
        self.amount = a
        self.exType = i
        self.payed_by = p
        self.year_spent = y


class Debt(models.Model):
    transactionID = models.CharField(max_length=10, unique=True)
    amount = models.FloatField()
    intrest = models.FloatField()
    debtor = models.ForeignKey(User, null=False, related_name='debts', on_delete='CASCADE')
    date_acquired = models.DateField()
    year_payed = models.IntegerField()

    def __init__(self, t, a, i, p, y):
        self.transactionID= t
        self.amount = a
        self.intrest = i
        self.debtor = p
        self.year_payed = y


class Investment(models.Model):
    transactionID = models.CharField(max_length=10, unique=True)
    amount_inv = models.FloatField()
    amount_returned = models.FloatField()
    investor = models.ForeignKey(User, null=False, related_name='investments', on_delete='CASCADE')
    date_acquired = models.DateField()
    year_payed = models.IntegerField()

    def __init__(self, t, a1, a2, i, p, y):
        self.transactionID= t
        self.amount_inv = a1
        self.amount_returned = a2
        self.intrest = i
        self.date_acquired = d
        self.year_payed = y
