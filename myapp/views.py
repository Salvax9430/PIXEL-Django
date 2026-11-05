from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import OrderForm, ProductForm, RegistrationForm, ReviewForm
from .models import DriverProfile, Order, Product, Profile


def profile_for(user):
    return Profile.objects.filter(user=user).first()


def index(request):
    products = Product.objects.filter(active=True).select_related("farmer__user")[:4]
    return render(request, "home.html", {"featured_products": products, "active_listings": Product.objects.filter(active=True).count()})


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


def marketplace(request):
    products = Product.objects.filter(active=True).select_related("farmer__user").annotate(review_average=Avg("reviews__rating"))
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    county = request.GET.get("county", "")
    if query:
        products = products.filter(name__icontains=query)
    if category:
        products = products.filter(category=category)
    if county:
        products = products.filter(county__iexact=county)
    return render(request, "marketplace.html", {"products": products, "listing_count": products.count(), "query": query, "selected_category": category, "selected_county": county})


@login_required
def dashboard(request):
    profile = profile_for(request.user)
    orders = Order.objects.filter(buyer=profile).select_related("product") if profile else Order.objects.none()
    farmer_products = Product.objects.filter(farmer=profile) if profile else Product.objects.none()
    revenue = orders.filter(status="complete").aggregate(total=Sum("quantity_kg"))["total"] or Decimal("0")
    return render(request, "dashboard.html", {"profile": profile, "orders": orders[:10], "farmer_products": farmer_products, "revenue_total": revenue, "active_orders": orders.exclude(status__in=("complete", "cancelled")).count()})


@login_required
def orders(request):
    profile = profile_for(request.user)
    user_orders = Order.objects.filter(buyer=profile).select_related("product", "driver__profile__user") if profile else Order.objects.none()
    return render(request, "orders.html", {"orders": user_orders, "order_count": user_orders.count(), "secured_total": sum((order.total for order in user_orders if order.payment_secured), Decimal("0"))})


def drivers(request):
    driver_profiles = DriverProfile.objects.filter(available=True).select_related("profile__user")
    return render(request, "drivers.html", {"drivers": driver_profiles})


def resources(request):
    return render(request, "resources.html")


def join(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user, role=form.cleaned_data["role"], phone=form.cleaned_data["phone"], county=form.cleaned_data["county"])
            if profile.role == "driver":
                DriverProfile.objects.create(profile=profile, vehicle_type="Not provided", capacity_kg=0)
            login(request, user)
            messages.success(request, "Your MavunoLink profile is ready.")
            return redirect("dashboard")
    else:
        form = RegistrationForm()
    return render(request, "join.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect(request.GET.get("next", "dashboard"))
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("myhome")


@login_required
def product_create(request):
    profile = profile_for(request.user)
    if not profile or profile.role != "farmer":
        messages.error(request, "Only farmer profiles can create produce listings.")
        return redirect("join")
    form = ProductForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        product = form.save(commit=False)
        product.farmer = profile
        product.save()
        messages.success(request, "Your listing is now live.")
        return redirect("listing_detail", product_id=product.pk)
    return render(request, "product_form.html", {"form": form})


def listing_detail(request, product_id):
    product = get_object_or_404(Product.objects.select_related("farmer__user"), pk=product_id, active=True)
    form = OrderForm(product=product)
    return render(request, "listing_detail.html", {"product": product, "order_form": form})


@login_required
def order_create(request, product_id):
    product = get_object_or_404(Product, pk=product_id, active=True)
    profile = profile_for(request.user)
    if not profile or profile.role != "buyer":
        messages.error(request, "Create a buyer profile to place an order.")
        return redirect("join")
    form = OrderForm(request.POST, product=product)
    if form.is_valid():
        order = form.save(commit=False)
        order.buyer = profile
        order.product = product
        order.unit_price = product.price_per_kg
        order.save()
        messages.success(request, "Order created. Choose payment and confirm delivery from Orders.")
        return redirect("orders")
    return render(request, "listing_detail.html", {"product": product, "order_form": form})


@login_required
def review_create(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    form = ReviewForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        review = form.save(commit=False)
        review.author = profile_for(request.user)
        review.product = product
        review.save()
    return redirect("listing_detail", product_id=product.pk)


def simple_page(request, page):
    pages = {
        "help": ("Help centre", "Find answers about buying, selling, payments and deliveries."),
        "safety": ("Safety & trust", "Our verification, escrow and community standards protect every trade."),
        "finance": ("Mavuno finance", "Flexible working capital for verified farmers and food businesses."),
        "agronomy": ("Smart agronomy", "Practical crop, weather and market guidance for better harvests."),
        "collective-buying": ("Collective buying", "Pool demand with nearby farmers and unlock better input prices."),
        "privacy": ("Privacy policy", "How MavunoLink handles and protects your information."),
        "terms": ("Terms of service", "The rules for using the MavunoLink network."),
    }
    title, description = pages.get(page, pages["help"])
    return render(request, "info.html", {"page_title": title, "page_description": description})
