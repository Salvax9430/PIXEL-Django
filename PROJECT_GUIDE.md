# MavunoLink Project Guide

## What this document is

This is the learning and handover guide for the MavunoLink project.

It explains:

1. What the project looked like at the beginning.
2. How the Django errors were found and fixed.
3. How the website grew from one simple page into a multi-page agriculture marketplace prototype.
4. What every important folder and file does.
5. How the pages connect to each other.
6. Which information is currently demonstration data.
7. How the project should become a real database-driven system later.

The guide is written step by step so that a beginner can follow it while reading the code.

This file is saved at:

```text
C:\Users\dell\OneDrive\Desktop\PIXEL-Django\pixeldjango\PROJECT_GUIDE.md
```

It is in the project root, next to `manage.py`.

---

## 1. The idea behind MavunoLink

MavunoLink is a planned Kenya agriculture network.

The main idea is:

```text
Farmer → MavunoLink → Buyer
                 ↘ Driver
```

The farmer should be able to sell directly.

The buyer should be able to find and buy produce directly.

The driver should be able to transport the produce.

The system should also help with:

- Trust and identity verification.
- Ratings and reviews.
- Delivery tracking.
- Secure payments and escrow.
- Agricultural knowledge.
- Crop and weather advice.
- Collective buying.
- Agricultural finance.
- AI assistance.
- Market prices.
- Dashboards for each type of user.

The current website is the visual and navigation foundation for this larger system.

---

## 2. Important distinction: prototype data versus real data

The current pages contain demonstration values so that the design can be viewed before the database is built.

Examples of current demonstration values include:

- `KSh 85 / kg` for avocados.
- `KSh 60 / kg` for tomatoes.
- `12,500+ farmers`.
- `1,284 verified drivers`.
- `KSh 248,600` revenue.
- Names such as David Kamau and Amina.
- Example order numbers such as `#MV-1048`.

These are not intended to be permanent application data.

When the database phase begins, these values should be replaced with:

```text
Database records
        ↓
Django models
        ↓
Views and querysets
        ↓
Template context
        ↓
HTML rendered with CSS
```

The CSS should remain mostly the same. The HTML should use Django template loops and variables instead of fixed example text.

For example, the current demonstration code may show:

```html
<h3>Hass Avocados</h3>
<strong>KSh 85</strong>
```

The future database-driven version should look more like:

```html
<h3>{{ product.name }}</h3>
<strong>KSh {{ product.price }}</strong>
```

And a list of products should eventually look like:

```html
{% for product in products %}
    <h3>{{ product.name }}</h3>
    <p>{{ product.county }}</p>
    <strong>KSh {{ product.price }}</strong>
{% empty %}
    <p>No products are available yet.</p>
{% endfor %}
```

This is an important design rule for the future:

> Users, products, prices, orders, drivers, ratings and dashboard values must come from the database, not be permanently typed into templates.

---

## 3. The starting Django project

The project is a Django project named `pixeldjango`.

The main command file is:

```text
manage.py
```

`manage.py` is the command-line doorway into Django.

It is used for commands such as:

```powershell
python manage.py runserver
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

The project configuration package is:

```text
pixeldjango/
```

The application package is:

```text
myapp/
```

In Django, a project is the whole website configuration, while an app is a reusable area of functionality.

---

## 4. The original problem that was found

The first Django check failed with this error:

```text
AttributeError: module 'myapp.views' has no attribute 'index'
```

The URL file was trying to use:

```python
path('', views.index, name='myhome')
```

But `views.py` did not contain an `index` function.

The old views file also defined `home` twice. The second definition replaced the first one, which meant the home page could not work correctly.

The fix was to create separate functions:

```python
def index(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")
```

This is a good Python lesson:

> If two functions have the same name, the later function replaces the earlier function.

---

## 5. The template problem that was found

The HTML files were initially placed directly in:

```text
myapp/
```

Django could not find them because the normal app template location is:

```text
myapp/templates/
```

The templates were moved to:

```text
myapp/templates/home.html
myapp/templates/about.html
myapp/templates/contact.html
```

The setting that makes this work is in `pixeldjango/settings.py`:

```python
'APP_DIRS': True,
```

`APP_DIRS = True` tells Django to look inside installed apps for a `templates` directory.

---

## 6. Django configuration

The main configuration file is:

```text
pixeldjango/settings.py
```

Important settings include:

### Installed apps

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
]
```

The important project-specific entry is:

```python
'myapp',
```

Without this line, Django would not treat `myapp` as an installed application.

### Templates

```python
'APP_DIRS': True,
```

This enables the app template folders explained above.

### Database

The initial project uses SQLite:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

SQLite is convenient for learning and early development.

Later, a production system could move to PostgreSQL.

### Static files

```python
STATIC_URL = 'static/'
```

This tells Django that browser assets such as CSS and JavaScript are served under the `/static/` URL path.

---

## 7. The final project structure

The important structure is:

```text
pixeldjango/
├── manage.py
├── db.sqlite3
├── PROJECT_GUIDE.md
├── myapp/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── url.py
│   ├── views.py
│   ├── migrations/
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── about.html
│   │   ├── contact.html
│   │   ├── marketplace.html
│   │   ├── dashboard.html
│   │   ├── orders.html
│   │   ├── drivers.html
│   │   ├── resources.html
│   │   ├── join.html
│   │   ├── listing_detail.html
│   │   └── info.html
│   └── static/
│       └── myapp/
│           ├── styles.css
│           └── app.js
└── pixeldjango/
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

The browser-facing CSS is not in the templates folder.

It is here:

```text
myapp/static/myapp/styles.css
```

The browser-facing JavaScript is here:

```text
myapp/static/myapp/app.js
```

---

## 8. URL routing

The application routes are in:

```text
myapp/url.py
```

The main project routes are in:

```text
pixeldjango/urls.py
```

The project URL file includes the app URL file:

```python
path('', include('myapp.url')),
```

This means Django checks `myapp/url.py` for the website pages.

The current routes are:

| URL | Name | Purpose |
|---|---|---|
| `/` | `myhome` | Main landing page |
| `/about/` | `about` | Original about page |
| `/contact/` | `my_contact` | Original contact page |
| `/marketplace/` | `marketplace` | Product marketplace |
| `/dashboard/` | `dashboard` | Farmer/business dashboard |
| `/orders/` | `orders` | Orders and payment overview |
| `/drivers/` | `drivers` | Driver directory and transport |
| `/resources/` | `resources` | Knowledge and market information |
| `/join/` | `join` | Farmer, buyer and driver onboarding |
| `/listing/avocados/` | `listing_detail` | Avocado listing detail |
| `/listing/tomatoes/` | `listing_detail` | Tomato listing detail |
| `/listing/maize/` | `listing_detail` | Maize listing detail |
| `/listing/mangoes/` | `listing_detail` | Mango listing detail |
| `/login/` | `login` | Login placeholder |
| `/help/` | `help` | Help centre placeholder |
| `/safety/` | `safety` | Safety and trust information |
| `/finance/` | `finance` | Finance information |
| `/agronomy/` | `agronomy` | Smart agronomy information |
| `/collective-buying/` | `collective_buying` | Group buying information |
| `/privacy/` | `privacy` | Privacy information |
| `/terms/` | `terms` | Terms information |

Using named URLs is safer than manually typing URL paths:

```html
{% url 'marketplace' %}
```

If the marketplace path changes later, Django can update links through the route name.

---

## 9. Views

The application views are in:

```text
myapp/views.py
```

At this stage, most views render a template:

```python
def marketplace(request):
    return render(request, "marketplace.html")
```

The listing detail view is already prepared for flexible data:

```python
def listing_detail(request, product="avocados"):
    products = {
        "avocados": (...),
        "tomatoes": (...),
        "maize": (...),
        "mangoes": (...),
    }
    product_data = products.get(product, products["avocados"])
    return render(request, "listing_detail.html", {"product": product_data})
```

This is a temporary bridge between a static prototype and a database.

Later, the dictionary should be replaced by a database query such as:

```python
product = get_object_or_404(Product, slug=product_slug)
```

The template can continue receiving a variable called `product`, so the visual layer does not need to be rebuilt.

---

## 10. Shared template layout

The shared layout is:

```text
myapp/templates/base.html
```

It contains:

- The top network status bar.
- The MavunoLink logo.
- Shared navigation.
- Login and join links.
- Shared footer.
- Static CSS loading.

Other pages inherit from it:

```django
{% extends "base.html" %}
```

Then they provide their own content:

```django
{% block content %}
    <!-- page-specific HTML -->
{% endblock %}
```

This avoids copying the header and footer into every page.

It also means that changing the navigation once updates the entire website.

---

## 11. Main pages and what they represent

### `home.html`

The main public landing page.

It introduces:

- The MavunoLink mission.
- Direct farmer-to-buyer trade.
- Product cards.
- Trust and verification.
- A dashboard preview.
- Driver delivery preview.
- Smart agronomy.
- Collective buying.
- Secure finance.
- AI assistant interface.

### `marketplace.html`

The marketplace workspace.

It includes:

- Product search area.
- County selector.
- Product categories.
- Quality filters.
- Product cards.
- Source farm information.
- Minimum order.
- Price per kilogram.
- Links to product detail pages.

The current filter controls are visual prototype controls. The next phase should connect them to GET parameters and database querysets.

### `listing_detail.html`

The individual product page.

It includes:

- Product name.
- County.
- Farm name.
- Price.
- Minimum order.
- Rating.
- Trust statements.
- Start-order action.
- Delivery action.

### `dashboard.html`

The farmer or business command centre.

It includes:

- Revenue.
- Active orders.
- Trust score.
- Sales chart.
- Latest orders.
- Quick actions.
- Suggested next action.

Later, these values must be calculated from orders and payments.

### `orders.html`

The order and payment workspace.

It includes:

- Awaiting payment.
- Orders in transit.
- Completed value.
- Escrow protection.
- Order rows.
- Driver tracking link.
- Payment protection information.

### `drivers.html`

The logistics page.

It includes:

- Verified driver count.
- On-time delivery rate.
- County coverage.
- Driver profiles.
- Vehicle type.
- Vehicle capacity.
- Estimated price.
- Request driver action.

### `resources.html`

The knowledge hub.

It includes:

- Featured agriculture guide.
- Agronomy topic.
- Business and finance topic.
- Logistics topic.
- Market price pulse.
- AI farming assistant.

### `join.html`

The registration entry page.

It asks whether a person is:

- A farmer or producer.
- A buyer.
- A driver or logistics partner.

The current continue action leads to the dashboard as a prototype. In the real system, it should lead to a registration form, account creation and verification workflow.

### `info.html`

This is a reusable information page for:

- Login.
- Help centre.
- Safety.
- Finance.
- Agronomy.
- Collective buying.
- Privacy.
- Terms.

The page title and description are passed into the template from the view.

---

## 12. CSS and visual design

The main stylesheet is:

```text
myapp/static/myapp/styles.css
```

Every template that uses static assets starts with:

```django
{% load static %}
```

And loads the stylesheet:

```html
<link rel="stylesheet" href="{% static 'myapp/styles.css' %}">
```

The stylesheet defines:

- MavunoLink colours.
- Typography.
- Buttons.
- Cards.
- Product grids.
- Dashboard panels.
- Tables.
- Driver maps.
- Responsive layouts.
- Mobile navigation.
- Information pages.
- Listing detail pages.

The main design tokens are near the beginning:

```css
:root {
    --ink: #17231b;
    --green: #215c3c;
    --bright: #c8f05d;
    --cream: #f6f5ee;
    --sand: #e7deca;
}
```

These variables make it easier to change the whole brand later.

For example, changing `--green` changes many green areas at once.

---

## 13. JavaScript and current interactions

The JavaScript file is:

```text
myapp/static/myapp/app.js
```

Current interactions include:

- Opening and closing the Mavuno AI chat panel.
- Filtering homepage products by category.
- Saving and unsaving favourite listings.
- Filling chat suggestions into the AI input.
- Showing a prototype AI response.
- Opening mobile navigation.

These are browser-only interactions right now.

They do not yet save data to a database.

Later, JavaScript can use Django forms or API requests:

```javascript
fetch("/api/products/")
```

But the server must validate and save the data. Browser JavaScript alone is not enough for secure data storage.

---

## 14. Why all values should become database data

A real MavunoLink system will need models such as:

```text
User
FarmerProfile
BuyerProfile
DriverProfile
County
Farm
Product
ProductImage
Inventory
Order
OrderItem
Payment
Delivery
Rating
Review
Notification
Conversation
Message
MarketPrice
CropGuide
VerificationRecord
FinanceApplication
CollectiveBuyGroup
```

Possible relationships:

```text
User 1──1 FarmerProfile
FarmerProfile 1──many Product
BuyerProfile 1──many Order
Order 1──many OrderItem
Order 1──1 Delivery
DriverProfile 1──many Delivery
Order 1──many Rating
```

Example future `Product` model:

```python
class Product(models.Model):
    farmer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products",
    )
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    county = models.CharField(max_length=80)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_kg = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_order_kg = models.DecimalField(max_digits=10, decimal_places=2)
    available_from = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

Then a marketplace view could use:

```python
products = Product.objects.filter(is_active=True)
return render(request, "marketplace.html", {"products": products})
```

The template could loop through those products.

The CSS cards would continue to style the output.

---

## 15. What “live” means in the future

“Live” can mean several different things:

### Live database values

Every page reads current records from the database.

### Live order status

An order changes from:

```text
Pending → Confirmed → Assigned → In transit → Delivered
```

### Live driver location

The driver app sends location updates, and the buyer sees a map.

### Live market prices

Prices are updated from:

- Farmer listings.
- Buyer demand.
- Market officers.
- Approved price feeds.

### Live notifications

Users receive messages when:

- An order is placed.
- A driver accepts a job.
- A payment is received.
- A delivery is close.
- A buyer sends a message.

Possible future technologies include:

- Django Channels and WebSockets.
- A task queue such as Celery.
- Redis.
- A mapping provider.
- SMS or WhatsApp integrations.
- Mobile money payment integration.

These are future integrations, not yet active in this prototype.

---

## 16. Future registration workflow

The registration process should eventually be:

```text
Choose role
    ↓
Enter phone and email
    ↓
Verify phone
    ↓
Enter location and county
    ↓
Add identity details
    ↓
Complete role profile
    ↓
Wait for verification if required
    ↓
Use dashboard
```

Farmer registration fields may include:

- Full name.
- Phone number.
- National identity verification.
- County.
- Sub-county.
- Farm name.
- Farm size.
- Crops grown.
- Available harvest dates.
- Payment details.

Buyer registration fields may include:

- Business name.
- Buyer type.
- Delivery locations.
- Typical products.
- Weekly volume.
- Payment method.

Driver registration fields may include:

- Full name.
- Phone number.
- Driving licence.
- Vehicle registration.
- Vehicle type.
- Capacity.
- Refrigeration availability.
- Operating counties.
- Insurance documents.

---

## 17. Future order calculation

The current site displays example order values.

The real system should calculate:

```text
Item subtotal
+ transport fee
+ service fee if applicable
- discount
= total
```

For example:

```python
subtotal = quantity_kg * price_per_kg
total = subtotal + delivery_fee - discount
```

All currency values should be calculated on the server, not trusted from the browser.

The database should store the final agreed values on the order so that later price changes do not rewrite old orders.

---

## 18. Future security requirements

Before real users are added, the project should implement:

- Django authentication.
- Password hashing through Django.
- Phone verification.
- Role-based permissions.
- Farmer ownership checks.
- Buyer order permissions.
- Driver delivery permissions.
- CSRF protection.
- Secure payment callbacks.
- Input validation.
- File upload validation.
- Rate limiting.
- Audit logs.
- Secure production secret management.
- HTTPS.
- Restricted `ALLOWED_HOSTS`.
- Database backups.

Never trust:

- A price sent from a browser.
- A user ID sent from a browser.
- A delivery status sent from a browser.
- A payment status sent from a browser.

The server must check those values.

---

## 19. Commands used to verify the project

From the project directory:

```powershell
cd "C:\Users\dell\OneDrive\Desktop\PIXEL-Django\pixeldjango"
```

Run the Django system check:

```powershell
python manage.py check
```

Start the development server:

```powershell
python manage.py runserver
```

Open the website:

```text
http://127.0.0.1:8000/
```

Run database migrations later:

```powershell
python manage.py makemigrations
python manage.py migrate
```

Create an admin user later:

```powershell
python manage.py createsuperuser
```

---

## 20. Validation already completed

The following pages were tested and returned HTTP 200:

```text
/
/about/
/contact/
/marketplace/
/dashboard/
/orders/
/drivers/
/resources/
/join/
/listing/avocados/
/listing/tomatoes/
/listing/maize/
/listing/mangoes/
/login/
/help/
/safety/
/finance/
/agronomy/
/collective-buying/
/privacy/
/terms/
```

The Django system check passed:

```text
System check identified no issues (0 silenced).
```

The project was also checked for dead links.

The literal placeholder links:

```html
href="#"
```

were removed from the templates.

---

## 21. Recommended next development order

When development continues, build in this order:

### Step 1: Create user accounts

Use Django authentication and role profiles.

### Step 2: Create farmer and product models

Allow farmers to create, edit and deactivate listings.

### Step 3: Replace marketplace demo records

Query products from the database and use template loops.

### Step 4: Add buyer ordering

Create a cart, order items and calculated totals.

### Step 5: Add driver workflow

Allow drivers to accept, update and complete deliveries.

### Step 6: Add payments

Integrate a Kenyan payment provider and server-side callbacks.

### Step 7: Add ratings

Allow ratings only after completed orders.

### Step 8: Add notifications and chat

Add messages and real-time updates.

### Step 9: Add maps and tracking

Connect locations and delivery progress.

### Step 10: Add AI carefully

Use AI for suggestions and explanations, but keep important decisions and financial actions under server validation.

---

## 22. Final summary

MavunoLink has moved through these stages:

```text
Broken route
    ↓
Working Django views
    ↓
Correct template folders
    ↓
Styled landing page
    ↓
Shared base layout
    ↓
Multiple connected pages
    ↓
Product detail routes
    ↓
Dashboard, orders and logistics flows
    ↓
Knowledge, finance and onboarding sections
    ↓
Ready foundation for database-backed development
```

The website is currently a strong frontend prototype with connected navigation and reusable styling.

The next major change is not to redesign the pages again. It is to connect the pages to real Django models, authenticated users, validated forms, calculated orders and live services.

