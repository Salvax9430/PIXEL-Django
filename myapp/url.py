from django.urls import path

from myapp import views
urlpatterns = [
    path('', views.index, name='myhome'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='my_contact'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('orders/', views.orders, name='orders'),
    path('drivers/', views.drivers, name='drivers'),
    path('resources/', views.resources, name='resources'),
    path('join/', views.join, name='join'),
    path('listing/new/', views.product_create, name='product_create'),
    path('listing/<int:product_id>/', views.listing_detail, name='listing_detail'),
    path('listing/<int:product_id>/order/', views.order_create, name='order_create'),
    path('listing/<int:product_id>/review/', views.review_create, name='review_create'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('help/', views.simple_page, {'page': 'help'}, name='help'),
    path('safety/', views.simple_page, {'page': 'safety'}, name='safety'),
    path('finance/', views.simple_page, {'page': 'finance'}, name='finance'),
    path('agronomy/', views.simple_page, {'page': 'agronomy'}, name='agronomy'),
    path('collective-buying/', views.simple_page, {'page': 'collective-buying'}, name='collective_buying'),
    path('privacy/', views.simple_page, {'page': 'privacy'}, name='privacy'),
    path('terms/', views.simple_page, {'page': 'terms'}, name='terms'),
]
   