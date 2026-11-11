from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from plans.models import TiffinPlan, Tag
from orders.models import Order, Delivery
from accounts.models import User, UserProfile
from .forms import TiffinPlanModelForm


def lab_demo_home(request):
    """
    Function-based view demonstrating Module 2 Request-Response Cycle and Context Passing.
    """
    context = {
        'total_plans': TiffinPlan.objects.count(),
        'total_orders': Order.objects.count(),
        'total_users': User.objects.count(),
        'total_tags': Tag.objects.count(),
    }
    return render(request, 'lab_demo/home.html', context)


def lab_demo_plans(request):
    """
    Demonstrating DTL loop tags, filters, and ORM QuerySets with filtering (Module 2 & 4).
    """
    queryset = TiffinPlan.objects.all().prefetch_related('tags').order_by('meal_type', 'price')

    meal_type = request.GET.get('meal_type')
    duration = request.GET.get('duration')

    if meal_type:
        queryset = queryset.filter(meal_type=meal_type)
    if duration:
        queryset = queryset.filter(duration=duration)

    context = {
        'plans': queryset,
    }
    return render(request, 'lab_demo/plans_list.html', context)


def lab_demo_plan_create(request):
    """
    Demonstrating Django ModelForm, CSRF protection, and server-side validation (Module 4 & 5).
    """
    if request.method == 'POST':
        form = TiffinPlanModelForm(request.POST)
        if form.is_valid():
            new_plan = form.save()
            messages.success(request, f"Meal Plan '{new_plan.title}' created successfully via ModelForm!")
            return redirect('lab-demo-plans')
    else:
        form = TiffinPlanModelForm()

    return render(request, 'lab_demo/plan_form.html', {'form': form})


def lab_demo_relationships(request):
    """
    Demonstrating 1:1, 1:N, N:1, N:M model relationships and relational queries (Module 4).
    """
    sample_orders = Order.objects.all().select_related('user', 'plan').prefetch_related('deliveries')[:10]

    context = {
        'total_profiles': UserProfile.objects.count(),
        'total_deliveries': Delivery.objects.count(),
        'total_orders': Order.objects.count(),
        'total_tags': Tag.objects.count(),
        'sample_orders': sample_orders,
    }
    return render(request, 'lab_demo/relationships.html', context)


def lab_demo_search(request):
    """
    Demonstrating Asynchronous AJAX Search with JavaScript and dynamic DOM rendering (Module 6).
    """
    initial_plans = TiffinPlan.objects.filter(is_active=True).order_by('meal_type', 'price')[:10]
    context = {
        'initial_plans': initial_plans,
        'initial_count': TiffinPlan.objects.filter(is_active=True).count(),
    }
    return render(request, 'lab_demo/search.html', context)
