from django.urls import path
from .views import SignUp, CustomLoginView

app_name = 'users'

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
]