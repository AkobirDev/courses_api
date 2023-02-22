from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.views import View
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsUser, ReadOnly
from users.models import CustomUser
from users.serializers import UserSerializer

from users.forms import RegisterForm, ProfileEditForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages

# ----------------  User Views for DRF  ---------------

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



# ----------------  User Views for Django  ---------------

class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {'register_form': register_form}
        return render(request, 'users/register.html', context=context)
    
    def post(self, request):
        register_form = RegisterForm(data=request.POST)
        if register_form.is_valid():
            register_form.save()
        else:
            context = {'register_form': register_form}
            return render(request, 'users/register.html', context=context)
        return redirect('users:login')
    
class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        context = {'login_form': login_form}
        return render(request, 'users/login.html', context)
    
    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, "You have successfully logged in.")
        else:
            context = {'login_form': login_form}
            return render(request, 'users/login.html', context)
        return redirect('landing_page')


class LogOutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'You have successfully Logged out.')
        return redirect('landing_page')

class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('users:login')
        context = {'user': request.user}
        return render(request, 'users/profile.html', context=context)
        
class ProfileEditView(View):
    def get(self, request):
        profile_edit_form = ProfileEditForm(instance=request.user)
        context = {'profile_edit_form': profile_edit_form}
        return render(request, 'users/profile_edit.html', context=context)

    def post(self, request):
        profile_edit_form = ProfileEditForm(
            instance=request.user, 
            data=request.POST, 
            files=request.FILES)
        if profile_edit_form.is_valid():
            profile_edit_form.save()
            messages.success(request, 'Changes are successfully changed.')
        else:
            context = {'profile_edit_form': profile_edit_form}
            return render(request, 'users/profile_edit.html', context=context)
        return redirect('users:profile')
