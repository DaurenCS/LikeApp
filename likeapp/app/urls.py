from django.urls import path
from .views import RegisterView, OppositeGenderProfilesView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profiles/opposite-gender/', OppositeGenderProfilesView.as_view(), name='opposite-gender-profiles'),
]