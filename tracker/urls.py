from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('upload/', views.upload_transactions, name='upload_transactions'),
    path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(template_name='tracker/login.html'), name='login'),  # Login URL
]