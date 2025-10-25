from rest_framework import serializers
from .models import Excursion, Poll

class ExcursionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Excursion
        fields = ['id', 'date', 'guide', 'n_visitors', 'phone', 'poll']

class PollSerializer(serializers.ModelSerializer):
    excursions = ExcursionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'week_start', 'week_end', 'is_active', 'excursions']