from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Count

from .models import Ticket, Reply
from .serializers import TicketSerializer, ReplySerializer


class HealthView(APIView):
    def get(self, request):
        return Response({"status": "ok"})


class TicketListCreateView(APIView):
    def get(self, request):
        items = Ticket.objects.all()

        q = request.query_params.get('q')
        if q:
            items = items.filter(subject__icontains=q)

        status_filter = request.query_params.get('status')
        if status_filter:
            items = items.filter(status=status_filter)

        return Response(TicketSerializer(items, many=True).data)

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        field, messages = next(iter(serializer.errors.items()))
        return Response({"error": str(messages[0]), "field": field}, status=status.HTTP_400_BAD_REQUEST)


class TicketDetailView(APIView):
    def get(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        return Response(TicketSerializer(ticket).data)

    def patch(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        serializer = TicketSerializer(ticket, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        field, messages = next(iter(serializer.errors.items()))
        return Response({"error": str(messages[0]), "field": field}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReplyListCreateView(APIView):
    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        replies = ticket.replies.all()
        return Response(ReplySerializer(replies, many=True).data)

    def post(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, pk=ticket_id)

        if ticket.status == 'closed':
            return Response(
                {"error": "Нельзя ответить на закрытое обращение", "field": "status"},
                status=status.HTTP_409_CONFLICT
            )

        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ticket=ticket)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatsView(APIView):
    def get(self, request):
        stats = Ticket.objects.annotate(reply_count=Count('replies')).values('id', 'subject', 'reply_count')
        return Response(list(stats))