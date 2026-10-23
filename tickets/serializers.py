from rest_framework import serializers

class TicketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    subject = serializers.CharField(max_length=200, allow_blank=False)
    description = serializers.CharField(max_length=500, allow_blank=False)
    status = serializers.ChoiceField(choices=["open", "closed"], default="open")