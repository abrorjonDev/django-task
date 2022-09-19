from django.urls import path


from .views import (
    HomeView, StartupCreateView, StartupUpdateView, StartupDetailView,
    RevenueView, RevenueUpdateView, RevenueDeleteView,
    RevenueFieldCreateView,
)

app_name = "startups"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('startups/create/', StartupCreateView.as_view(), name="startup_create"),
    path('startups/update/<int:pk>/', StartupUpdateView.as_view(), name="startup_update"),
    path('startups/detail/<int:pk>/', StartupDetailView.as_view(), name="startup_detail"),

    path('revenues/<int:startup_id>/', RevenueView.as_view(), name="revenues"),
    path('revenues/update/<int:pk>/', RevenueUpdateView.as_view(), name="revenues_update"),
    path('revenues/delete/<int:pk>/', RevenueDeleteView.as_view(), name="revenues_delete"),

    path('revenues/fields/<int:revenue_id>/create/', RevenueFieldCreateView.as_view(), name="revenues_fields_create"),
    
]