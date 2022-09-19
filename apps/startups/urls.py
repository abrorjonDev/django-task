from django.urls import path


from .views import (
    HomeView, startup_create, StartupUpdateView, StartupDeleteView,
    ReportListView, report_create, expense_create

)
app_name = "startups"
urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('startups/create/', startup_create, name="startup_create"),
    path('startups/<int:pk>/update/', StartupUpdateView.as_view(), name="startup_update"),
    path('startups/<int:pk>/delete/', StartupDeleteView.as_view(), name="startup_delete"),

    path('reports/<int:startup_id>/', ReportListView.as_view(), name="reports"),
    path('reports/<int:startup_id>/add-revenue/', report_create, name="revenue-add"),
    path('reports/<int:startup_id>/add-expense/', expense_create, name="expense-add"),
    
    
    path('admin/', HomeView.as_view(), name="admin")
]