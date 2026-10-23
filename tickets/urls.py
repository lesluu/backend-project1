from django.urls import path
from .views import HealthView, TicketListCreateView, TicketDetailView

urlpatterns = [
    path("health", HealthView.as_view()),
    path("api/tickets", TicketListCreateView.as_view()),
    path("api/tickets/<int:pk>", TicketDetailView.as_view()),
]