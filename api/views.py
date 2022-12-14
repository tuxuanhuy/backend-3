from django.shortcuts import render

from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import *
from .models import *

from datetime import datetime

# Create your views here.

# List all Users
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


# Get detail of User 
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    


# List all Shifts
class ShiftList(generics.ListCreateAPIView):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    # permission_classes = [permissions.IsAuthenticated]


# Search for Shifts in a Date
class ShiftSearch(generics.ListAPIView):
    serializer_class = ShiftSerializer
    
    def get_queryset(self):
        queryset = Shift.objects.all()
        date = self.request.query_params.get('date')
        if date is not None:
            queryset = queryset.filter(date = date)
        return queryset


# Get detail of Shift
class ShiftDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer


# List all Shifts of an User
class UserShift(generics.ListAPIView):
    serializer_class = ShiftSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Shift.objects.filter(user = pk)




# Search for Today
class ShiftToday(generics.ListAPIView):
    serializer_class = ShiftSerializer
    
    def get_queryset(self):
        queryset = Shift.objects.all()
        date = datetime.now().date()
        if date is not None:
            queryset = queryset.filter(date = date)
        return queryset


class UserPicture(generics.ListAPIView):
    serializer_class = FaceSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Face.objects.filter(user = pk)


# Search for Shifts in Range
class ShiftRange(generics.ListAPIView):
    serializer_class = ShiftSerializer

    def get_queryset(self):
        queryset = Shift.objects.all()
        start_time = datetime(2022, 12, 14)
        end_time = datetime(2022, 12, 15)

        queryset = queryset.filter(start_time__range=[start_time, end_time])
        return queryset


# Login API
class LoginAPI(generics.GenericAPIView):

    # Define methods
    model = User
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                username = serializer.validated_data['username'],
                password = serializer.validated_data['password']
            )

            if user:
                refresh = TokenObtainPairSerializer.get_token(user)
                data = {
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token)
                }
                return Response(data, status=status.HTTP_200_OK)

            return Response({
                'error_message': 'Username or password is incorrect!',
                'error_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'error_messages': serializer.errors,
            'error_code': 400
        }, status=status.HTTP_400_BAD_REQUEST)


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)