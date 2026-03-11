from django.urls import path
from . import views

urlpatterns = [

    path('', views.dashboard, name='dashboard'),


    path('portfolio/create/', views.create_portfolio, name='create_portfolio'),

    path('portfolio/<int:portfolio_id>/add-asset/', views.add_asset, name='add_asset'),
]