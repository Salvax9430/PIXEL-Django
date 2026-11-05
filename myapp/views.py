from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")


def marketplace(request):
    return render(request, "marketplace.html")


def dashboard(request):
    return render(request, "dashboard.html")


def orders(request):
    return render(request, "orders.html")


def drivers(request):
    return render(request, "drivers.html")


def resources(request):
    return render(request, "resources.html")


def join(request):
    return render(request, "join.html")


def listing_detail(request, product="avocados"):
    products = {
        "avocados": ("Hass Avocados", "Green Hills Farm", "Murang'a", "85", "120 kg"),
        "tomatoes": ("Grade 1 Tomatoes", "Wambui Growers", "Kirinyaga", "60", "80 kg"),
        "maize": ("Dry White Maize", "Eldoret Co-op", "Uasin Gishu", "68", "500 kg"),
        "mangoes": ("Apple Mangoes", "Kilili Orchards", "Makueni", "95", "200 kg"),
    }
    product_data = products.get(product, products["avocados"])
    return render(request, "listing_detail.html", {"product": product_data})


def simple_page(request, page):
    pages = {
        "login": ("Log in to MavunoLink", "Access your marketplace, orders and farm dashboard."),
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
