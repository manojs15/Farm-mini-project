# views.py
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .forms import UserRegistrationForm, FarmerRegistrationForm,FarmForm,CropForm,LivestockForm,ExpenseForm,BudgetForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Farm,Crop,Livestock,Expense
from django.db import models


@login_required
def register_view(request):
    if request.method == 'POST':
        farmer_form = FarmerRegistrationForm(request.POST)
        if farmer_form.is_valid():
            # Check if the user is authenticated (logged in)
            if request.user.is_authenticated:
                farmer = farmer_form.save(commit=False)
                farmer.user = request.user
                farmer.save()
                return redirect('app:dashboard')
            else:
                # Handle the case where the user is not logged in
                # Redirect to a login page or display an error message
                return redirect('app:signup')  # Example redirect to login page
    else:
        farmer_form = FarmerRegistrationForm()
    return render(request, 'register.html', {'farmer_form': farmer_form})

#-------------------------------------------------------

def signup_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('app:login')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'signup.html', {'user_form': user_form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to a success page or wherever you want
            return redirect('app:dashboard')  # Replace 'success_page' with the URL name of your success page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

#---------------------------------------------------------------------

def dashboard_view(request):
     # Logic to retrieve total farms
    total_farms = Farm.objects.count()

    # Logic to retrieve total crops
    total_crops = Crop.objects.count()

    # Logic to retrieve total livestock
    total_livestock = Livestock.objects.count()

    context = {
        'total_farms': total_farms,
        'total_crops': total_crops,
        'total_livestock': total_livestock,
    }

    return render(request, 'dashboard.html',context)

#--------------------------------------------------------------------

def farm_list(request):
    farms = Farm.objects.all()
    return render(request, 'farm_mgmt/farm_list.html', {'farms': farms})

def view_farm(request, farm_id):
    farm = get_object_or_404(Farm, farm_id=farm_id)
    return render(request, 'farm_mgmt/view_farm.html', {'farm': farm})

def add_farm(request):
    if request.method == 'POST':
        farm_form = FarmForm(request.POST)
        if farm_form.is_valid():
            farm = farm_form.save(commit=False)
            farm.farmer = request.user.farmer  # Assign the current user's farmer profile to the farm
            farm.save()
            return redirect('app:farm_list')
    else:
        farm_form = FarmForm()
    return render(request, 'farm_mgmt/add_page.html', {'farm_form': farm_form})     

def edit_farm(request, farm_id):
    farm = get_object_or_404(Farm, farm_id=farm_id)
    if request.method == 'POST':
        form = FarmForm(request.POST, instance=farm)
        if form.is_valid():
            form.save()
            return redirect('app:farm_list')
    else:
        form = FarmForm(instance=farm)
    return render(request, 'farm_mgmt/edit_farm.html', {'form': form, 'farm': farm})

def delete_farm(request, farm_id):
    farm = get_object_or_404(Farm, farm_id=farm_id)
    if request.method == 'POST':
        farm.delete()
        return redirect('app:farm_list')
    return render(request, 'farm_mgmt/delete_farm.html', {'farm': farm})
#---------------------------------------------------------------------
                        #C-R-O-P-S
def crop_list(request):
    crops = Crop.objects.all()
    return render(request, 'crop_mgmt/crop_list.html', {'crops': crops})

def view_crop(request, crop_id):
    crop = get_object_or_404(Crop, crop_id=crop_id)
    return render(request, 'crop_mgmt/view_crop.html', {'crop': crop, 'crop_id':crop_id})

def add_crop(request):
    if request.method == 'POST':
        crop_form = CropForm(request.POST)
        if crop_form.is_valid():
            crop = crop_form.save(commit=False)
            farmer_farms = request.user.farmer.farms.all()  # Access all farms of the logged-in farmer
            if farmer_farms:
                crop.farm = farmer_farms.first()  # Assign the first farm of the logged-in farmer
                crop.save()
                return redirect('app:crop_list')
            else:
                # Handle the case where the farmer has no farms
                # You might want to redirect to a page to add a farm or display an error message
                return redirect('app:add_farm')  # Example redirect to add farm page
    else:
        crop_form = CropForm()
    return render(request, 'crop_mgmt/add_crop.html', {'crop_form': crop_form})


def edit_crop(request, crop_id):
    crop = get_object_or_404(Crop, crop_id=crop_id)
    if request.method == 'POST':
        crop_form = CropForm(request.POST, instance=crop)
        if crop_form.is_valid():
            crop_form.save()
            return redirect('app:crop_list')
    else:
        crop_form = CropForm(instance=crop)
    return render(request, 'crop_mgmt/edit_crop.html', {'crop_form': crop_form, 'crop': crop})

def delete_crop(request, crop_id):
    crop = get_object_or_404(Crop, crop_id=crop_id)
    if request.method == 'POST':
        crop.delete()
        return redirect('app:crop_list')
    return render(request, 'crop_mgmt/delete_crop.html', {'crop': crop})


#-----------------------------------------------------------------------


def livestock_list(request):
    livestocks = Livestock.objects.all()
    return render(request, 'livestock_mgmt/livestock_list.html', {'livestocks': livestocks})

def view_livestock(request, livestock_id):
    livestock = get_object_or_404(Livestock, livestock_id=livestock_id)
    return render(request, 'livestock_mgmt/view_livestock.html', {'livestock': livestock, 'livestock_id':livestock_id})


def add_livestock(request):
    if request.method == 'POST':
        livestock_form = LivestockForm(request.POST)
        if livestock_form.is_valid():
            livestock = livestock_form.save(commit=False)
            farmer_farms = request.user.farmer.farms.all()  # Access all farms of the logged-in farmer
            if farmer_farms:
                livestock.farm = farmer_farms.first()  # Assign the first farm of the logged-in farmer
                livestock.save()
                return redirect('app:livestock_list')
            else:
                # Handle the case where the farmer has no farms
                # You might want to redirect to a page to add a farm or display an error message
                return redirect('app:add_farm')  # Example redirect to add farm page
    else:
        livestock_form = LivestockForm()
    return render(request, 'livestock_mgmt/add_livestock.html', {'livestock_form': livestock_form})


def edit_livestock(request, livestock_id):
    livestock = get_object_or_404(Livestock, livestock_id=livestock_id)
    if request.method == 'POST':
        livestock_form = LivestockForm(request.POST, instance=livestock)
        if livestock_form.is_valid():
            livestock_form.save()
            return redirect('app:livestock_list')
    else:
        livestock_form = LivestockForm(instance=livestock)
    return render(request, 'livestock_mgmt/edit_livestock.html', {'livestock_form': livestock_form, 'livestock': livestock})


def delete_livestock(request, livestock_id):
    livestock = get_object_or_404(Livestock, livestock_id=livestock_id)
    if request.method == 'POST':
        livestock.delete()
        return redirect('app:livestock_list')
    return render(request, 'livestock_mgmt/delete_livestock.html', {'livestock': livestock})

#----------------------------------------------------------------------------

def expense_list(request):
    expenses = Expense.objects.filter(farmer=request.user.farmer)
    return render(request, 'expense_mgmt/expense_list.html', {'expenses': expenses})

def add_expense(request):
    if request.method == 'POST':
        expense_form = ExpenseForm(request.POST)
        if expense_form.is_valid():
            expense = expense_form.save(commit=False)
            expense.farmer = request.user.farmer
            expense.save()

            messages.success(request, 'Expense added successfully!')
            return redirect('app:expense_list')
        else:
            messages.error(request, 'Failed to add expense. Please correct the errors.')
    else:
        expense_form = ExpenseForm()

    return render(request, 'expense_mgmt/add_expense.html', {'expense_form': expense_form})

def view_expense(request, expense_id):
    expense = get_object_or_404(Expense, expense_id=expense_id)
    return render(request, 'expense_mgmt/view_expense.html', {'expense': expense})

def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, expense_id=expense_id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('app:expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expense_mgmt/edit_expense.html', {'form': form, 'expense': expense})

def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, expense_id=expense_id)
    if request.method == 'POST':
        expense.delete()
        return redirect('app:expense_list')
    return render(request, 'expense_mgmt/delete_expense.html', {'expense': expense})

#---------------------------------------------------------------------------------
def expense_summary(request):
    # Get all expense types
    expense_types = Expense.objects.values_list('expense_type', flat=True).distinct()
    # Calculate total expenses, average expenses, and other metrics (replace with actual logic)
    total_expenses = Expense.objects.aggregate(total_expenses=models.Sum('amount'))['total_expenses'] or 0
    total_count = Expense.objects.count()
    average_expenses = total_expenses / total_count if total_count > 0 else 0
    # Calculate expenses by type
    expenses_by_type = [Expense.objects.filter(expense_type=expense_type).aggregate(total=models.Sum('amount'))['total'] or 0 for expense_type in expense_types]
    # Calculate expense distribution for pie chart
    total_amount = sum(expenses_by_type)
    expense_distribution = [float(amount) / float(total_amount) * 100 if total_amount > 0 else 0 for amount in expenses_by_type]
    expenses_by_type_str = [str(amount) for amount in expenses_by_type]
    context = {
        'total_expenses': total_expenses,
        'average_expenses': average_expenses,
        'expense_types': list(expense_types),
        'expenses_by_type': expenses_by_type_str,
        'expense_distribution': expense_distribution,
        # Add other metrics to the context
    }
    return render(request, 'exp_summary_mgmt/expense_summary.html', context)

def detailed_reports(request):
    # Retrieve filters from the request if available
    expense_type = request.GET.get('expense_type')
    farm_id = request.GET.get('farm_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    # Filter expenses based on provided filters
    expenses = Expense.objects.all()
    if expense_type:
        expenses = expenses.filter(expense_type=expense_type)
    if farm_id:
        expenses = expenses.filter(farm_id=farm_id)
    if start_date:
        expenses = expenses.filter(expense_date__gte=start_date)
    if end_date:
        expenses = expenses.filter(expense_date__lte=end_date)

    context = {
        'expenses': expenses,
    }
    return render(request, 'exp_summary_mgmt/detailed_reports.html', context)

def set_budget(request, expense_id):
    expense = Expense.objects.get(expense_id=expense_id)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('app:expense_list')  # Redirect to the expense list or another appropriate page
    else:
        form = BudgetForm(instance=expense)
    return render(request, 'exp_summary_mgmt/set_budget.html', {'form': form, 'expense': expense})

def financial_reports(request):
    # Retrieve necessary data for financial reports
    # You may need to customize this based on your specific requirements
    expenses = Expense.objects.all()
    total_expenses = sum(expense.amount for expense in expenses)
    context = {
        'total_expenses': total_expenses,
        'expenses': expenses,
    }
    return render(request, 'exp_summary_mgmt/financial_reports.html', context)