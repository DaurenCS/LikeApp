from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Profile
from .serializer import ProfileSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        gender = request.data.get('gender')

        if not all([username, password, email, gender]):
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        Profile.objects.create(user=user, gender=gender)
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

class OppositeGenderProfilesView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_profile = Profile.objects.get(user=self.request.user)
        user_gender = user_profile.gender
         
         
        opposite_gender = 'M' if user_gender == 'F' else 'F'
        return Profile.objects.filter(gender=opposite_gender)
