from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post, Comment, Board, Income, Expense, Investment, Debt
from .forms import NewPostForm, NewCommentForm
import matplotlib as mp
import numpy as npy
from django.contrib.auth.models import User
import string 
import random
import csv

# Create your views here.
def randomString(stringLength):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})

def finance(request):
    return render(request, 'finance.html')

def new_post(request):
    b_name = ''
    if request.GET.get('name'):
	    b_name = request.GET.get('name')
    board = Board.objects.get(name=b_name)
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            post_temp = form.save(commit=False)
            post_temp.board = board
            post_temp.created_by = user
            post_temp.save()
            '''post_temp = Post.objects.create(
                message=form.cleaned_data.get('message'),
                post=post_temp,
                created_by=user
            )'''
            return post(request)
            #return render(request, 'post.html')  # TODO: redirect to the created topic page
    else:
        form = NewPostForm()
    return render(request, 'new_post.html', {'form': form})

def new_comment(request):
    board = get_object_or_404(Comment)
    post = get_object_or_404(Post)
    user = User.object.first()
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        comment = form.save(commit=False)
        comment.board = board
        comment.post = post
        comment.created_by = user
        comment.save()
        comment = Comment.objects.create(
            message = form.cleaned_data.get('message'),
            comment = comment,
            created_by = user
        )
        return redirect('post.html')
    else:
        form = NewCommentForm()
    return render(request, 'new_comment.html', {'form': form})

def post(request):
    b_name = request.GET.get('name')
    posts = Post.objects.all()
	
    return render(request, 'post.html', {'posts': posts, 'b_name': b_name})


def view_posts(request):
    posts = Post.objects.all()
    comments = Comment.objects.all()
    return render(request, 'post.html', {'post': posts}, {'comment': comments})

def getFinances(request):
    incomes = Income.objects.filter(payed_to = request.user)
    expenses = Expense.objects.filter(payed_by = request.user)
    debts = Debt.objects.filter(debtor = request.user)
    investments = Investment.objects.filter(investor = request.user)

    return render(request, 'finance.html', {'income', incomes},{'expenses', expenses}, {'investments', investments}, {'debts', debts})

def queryFinances(request):
    incomes = Income.objects.get(payed_to = request.user)
    return render(request, 'inQuery.html', {'income': incomes})
    
    
def spending_bar(request, x, y):
    amounts = [0,0,0,0,0]
    expenses = Expense.objects.get(year_earned=x)
    for expense in expenses:
        if expense.exType == "Food":
            amounts[0] = expense.amount
        if expense.exType == "Utilities":
            amounts[1] = expense.amount
        if expense.exType == "Necessities":
            amounts[2] = expense.amount
        if expense.exType == "Education":
            amounts[3] = expense.amount
        if expense.exType == "Recreation":
            amounts[4] = expense.amount
        if expense.exType == "Other":
            amounts[5] = expense.amount

    objects = ['Food', 'Utilites', 'Necessities', 'Education', 'Recreation', 'Other']
    y = npy.arange(len(objects))
    mp.bar(y, amounts, align='center', alpha=0.5)
    mp.xticks(y, objects)
    mp.title("Spending", loc="center")
    mp.show()
    amounts = [0,0,0,0,0]
    expenses = Expense.objects.get(year_earned=y)
    for expense in expenses:
        if expense.exType == "Food":
            amounts[0] = expense.amount
        if expense.exType == "Utilities":
            amounts[1] = expense.amount
        if expense.exType == "Necessities":
            amounts[2] = expense.amount
        if expense.exType == "Education":
            amounts[3] = expense.amount
        if expense.exType == "Recreation":
            amounts[4] = expense.amount
        if expense.exType == "Other":
            amounts[5] = expense.amount

    objects = ['Food', 'Utilites', 'Necessities', 'Education', 'Recreation', 'Other']
    y = npy.arange(len(objects))
    mp.bar(y, amounts, align='center', alpha=0.5)
    mp.xticks(y, objects)
    mp.title("Spending", loc="center")
    mp.show() 

def income_plot(self):
    coordinates = []
    data=[]
    dates = []
    with open(self) as csvfile:
        readcsv = csv.reader(csvfile, delimiter=',')
        for row in readcsv:
            c = [row[4], row[1]]
            coordinates.append(c)
            date = row[4]
            data = npy.array(coordinates)
    x, y = data.T
    mp.scatter(x, y)
    mp.title("Income")
    mp.show()

def invest_bar(self):
    returns = Investment.objects.all()
    amounts = [0,0,0,0,0,0,0,0,0,0]
    years = []
    for inv in returns:
        years.append(inv.year_payed)
    years.sort()
    for inv in returns:
        i = years.index(inv.year_payed)
        amounts[i]+=inv.amount_inv
    y = npy.arange(years)
    mp.bar(y, amounts, align='center', alpha=0.5)
    mp.bar(y, amounts, align='center', alpha=0.5)
    mp.xticks(y, years)
    mp.title("Returns", loc="center")
    mp.show()    

def uploadInc(request):
    if request.method == 'POST':
        with open(request) as csvfile:
            readcsv = csv.reader(csvfile, delimiter=',')
            for row in csvfile:
                i = Income(
                transactionID = randomString(10),
                amount = row[1],
                inType = "Salary",
                payed_to = request.user,
                year_earned = row[0])
                i.save()
    return HttpResponse('File uploaded')

def uploadEx(request):
    if request.method == 'POST':
        with open(request) as csvfile:
            readcsv = csv.reader(csvfile, delimiter=',')
            for row in csvfile:
                i = Income(
                transactionID = randomString(10),
                amount = row[1],
                inType = "Salary",
                payed_to = request.user,
                year_earned = row[0])
                i.save()
    return HttpResponse('File uploaded')

def uploadInv(request):
    if request.method == 'POST':
        with open(request) as csvfile:
            readcsv = csv.reader(csvfile, delimiter=',')
            for row in csvfile:
                i = Investment(
                transactionID = randomString(10),
                amount_inv = row[1],
                year_payed = row[0])
                i.save()
    return HttpResponse('File uploaded')

def uploadDebt(request):
    if request.method == 'POST':
        with open(request) as csvfile:
            readcsv = csv.reader(csvfile, delimiter=',')
            for row in csvfile:
                i = Debt(
                transactionID = randomString(10),
                amount = row[1],
                intrest = 0,
                year_payed = row[0])
                i.save()      
    return HttpResponse('File uploaded')

def predict_return(self):
    invs = Investment.object.all()
    amt = 0
    i = 0
    for x in invs:
        i+=1
        amt +=x.amount_inv
    return amt/i 