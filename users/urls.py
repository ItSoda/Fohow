from django.urls import path, include
from django.conf import settings

from rest_framework import routers
from .views import UserModelViewSet, EmailVerificationAndUserUpdateView


app_name = 'users'

router = routers.DefaultRouter()
router.register(r'users', UserModelViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path("verify/<str:email>/<uuid:code>/", EmailVerificationAndUserUpdateView.as_view(), name='email_verify'),
    path('user/update/', EmailVerificationAndUserUpdateView.as_view(), name='user-update'),
]