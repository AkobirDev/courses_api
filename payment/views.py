from django.shortcuts import render
from payment.models import Payment
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from payment.serializers import PaymentSerializer
# Create your views here.

class PaymentView(ListAPIView):
    # queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_class = [IsAuthenticated]
    def get_queryset(self):
        queryset = Payment.objects.filter(user=self.request.user)
        return queryset
    