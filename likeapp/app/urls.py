from django.urls import path
from .views import RegisterView, OppositeGenderProfilesView, LoginView, LikeView, MatchesView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profiles/opposite-gender/', OppositeGenderProfilesView.as_view(), name='opposite-gender-profiles'),
    path('login/',LoginView.as_view(), name = 'login'),
    path('like/', LikeView.as_view(), name='like'),
    path('matches/', MatchesView.as_view(), name='matches'),
]