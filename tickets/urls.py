from django.urls import path
from .views import (
    HealthView, TicketListCreateView, TicketDetailView,
    ReplyListCreateView, StatsView
)

urlpatterns = [
    path("health", HealthView.as_view()),
    path("api/tickets", TicketListCreateView.as_view()),
    path("api/tickets/<int:pk>", TicketDetailView.as_view()),
    path("api/tickets/<int:ticket_id>/replies", ReplyListCreateView.as_view()),
    path("api/tickets/stats", StatsView.as_view()),
]