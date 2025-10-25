from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Excursion, Poll
from .serializers import ExcursionSerializer, PollSerializer
from datetime import datetime

class ExcursionListCreateView(generics.ListCreateAPIView):
    queryset = Excursion.objects.all()
    serializer_class = ExcursionSerializer

    def perform_create(self, serializer):
        serializer.save()

class ExcursionDetailView(generics.RetrieveAPIView):
    queryset = Excursion.objects.all()
    serializer_class = ExcursionSerializer

class PollListCreateView(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def perform_create(self, serializer):
        poll = serializer.save()
        week_start = poll.week_start
        week_end = poll.week_end
        excursions = Excursion.objects.filter(date__range=[week_start, week_end])
        for excursion in excursions:
            excursion.poll = poll
            excursion.save()

class PollDetailView(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer