from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .forms import TransactionForm, FileUploadForm
import pandas as pd
from django.contrib import messages

@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'tracker/dashboard.html', {'transactions': transactions})

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()
    return render(request, 'tracker/add_transaction.html', {'form': form})

@login_required
def upload_transactions(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            try:
                df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
                for _, row in df.iterrows():
                    Transaction.objects.create(
                        user=request.user,
                        category=row['category'],
                        amount=row['amount'],
                        description=row.get('description', ''),
                        date=row['date'],
                    )
                messages.success(request, "Transactions uploaded successfully!")
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f"Error processing file: {e}")
    else:
        form = FileUploadForm()
    return render(request, 'tracker/upload_transactions.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/signup.html', {'form': form})