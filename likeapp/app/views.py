from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Profile, ViewedProfiles, Like, Match
from .serializer import ProfileSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.core.paginator import Paginator
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q

# Create your views here.

class RegisterView(APIView):
    permission_classes = [AllowAny]

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

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        username = request.data.get('username')
        
        if not username:
            return Response({"error": "Username is required"}, status= status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.filter(username = username).first()

            if not user:
                return Response({"error": "You need register"}, status= status.HTTP_400_BAD_REQUEST)
            
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        
        except Exception as e:
             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.response import Response

class OppositeGenderProfilesView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
    
        user_profile = Profile.objects.get(user=self.request.user)
        user_gender = user_profile.gender

        opposite_gender = 'M' if user_gender == 'F' else 'F'

        viewed_profiles = ViewedProfiles.objects.filter(user=self.request.user).values_list('profile_id', flat=True)

        available_profiles = Profile.objects.filter(gender=opposite_gender).exclude(id__in=viewed_profiles)
        available_profiles = available_profiles.order_by('?') 

        page_size = 2
        page_number = int(self.request.query_params.get('page', 1))
        offset = (page_number - 1) * page_size

        return available_profiles[offset:offset + page_size]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        for profile in queryset:
            ViewedProfiles.objects.get_or_create(user=request.user, profile=profile)

        return Response(serializer.data)

class LikeView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def post(self, request):
        target_user_id = request.data.get("user_to")
        if not target_user_id:
            return Response({"error": "User to like is required"}, status=400) 
        
        try:
            target_user = User.objects.get(id=target_user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        
        if Like.objects.filter(user_from=request.user, user_to=target_user).exists():
            return Response({"message": "You already liked this user"}, status=400)
        
        Like.objects.create(user_from=request.user, user_to=target_user)


        if Like.objects.filter(user_from=target_user, user_to=request.user).exists():
            # Create a match
            Match.objects.create(user1=request.user, user2=target_user)
            return Response({"message": "It's a match!"}, status=200)

        return Response({"message": "Like recorded"}, status=200)
        

class MatchesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve all matches for the current user
        matches = Match.objects.filter(Q(user1=request.user) | Q(user2=request.user))
        matched_users = [
            match.user1 if match.user2 == request.user else match.user2 for match in matches
        ]
        matched_users_data = [{"id": user.id, "username": user.username} for user in matched_users]
        return Response(matched_users_data, status=200)