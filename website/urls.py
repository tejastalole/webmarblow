from django.urls import path

from website import views

app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('portfolio/<slug:slug>/', views.portfolio_detail, name='portfolio_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('quote/', views.quote, name='quote'),
]
