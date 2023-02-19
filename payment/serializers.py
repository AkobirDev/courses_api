from payment.models import Payment
from rest_framework import serializers

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'user', 'payment_method', 'get_enrolled_courses',
                  'get_total_price', 'created_at')