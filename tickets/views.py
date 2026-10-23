from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Ticket, store
from .serializers import TicketSerializer


class HealthView(APIView):
    def get(self, request):
        return Response({"status": "ok"})


class TicketListCreateView(APIView):
    def get(self, request):
        items = store.all()

        status_filter = request.query_params.get("status")
        if status_filter:
            items = [t for t in items if t.status == status_filter]

        limit = request.query_params.get("limit")
        offset = request.query_params.get("offset", 0)
        if limit is not None:
            try:
                limit = int(limit)
                offset = int(offset)
            except ValueError:
                return Response(
                    {"error": "limit и offset должны быть числами", "field": "limit"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            items = items[offset: offset + limit]

        return Response([t.to_dict() for t in items])

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if not serializer.is_valid():
            field, messages = next(iter(serializer.errors.items()))
            return Response(
                {"error": str(messages[0]), "field": field},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = serializer.validated_data
        ticket = Ticket(
            subject=data["subject"],
            description=data.get("description", ""),
            status=data.get("status", "open"),
        )
        store.add(ticket)
        return Response(ticket.to_dict(), status=status.HTTP_201_CREATED)


class TicketDetailView(APIView):
    def get(self, request, pk):
        ticket = store.get(pk)
        if ticket is None:
            return Response({"error": "not found", "field": "id"}, status=404)
        return Response(ticket.to_dict())

    def patch(self, request, pk):
        ticket = store.get(pk)
        if ticket is None:
            return Response({"error": "not found", "field": "id"}, status=404)

        serializer = TicketSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            field, messages = next(iter(serializer.errors.items()))
            return Response(
                {"error": str(messages[0]), "field": field},
                status=status.HTTP_400_BAD_REQUEST,
            )

        for key, value in serializer.validated_data.items():
            setattr(ticket, key, value)
        return Response(ticket.to_dict())

    def delete(self, request, pk):
        ticket = store.delete(pk)
        if ticket is None:
            return Response({"error": "not found", "field": "id"}, status=404)
        return Response(status=status.HTTP_204_NO_CONTENT)