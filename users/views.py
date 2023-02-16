from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsUser, ReadOnly
from users.models import CustomUser
from users.serializers import UserSerializer


User = get_user_model()


class UserView(viewsets.ViewSet):
    
    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)    
    
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk):
        user = User.objects.get(pk=pk)
        instance = user
        serializer = UserSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsUser | ReadOnly]
        
        return [permission() for permission in permission_classes]
