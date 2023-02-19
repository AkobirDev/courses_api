from rest_framework import serializers

from users.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'bio', 'avatar', 'is_teacher', 'get_paid_courses' )
        