from rest_framework.permissions import IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.services import EmailVerificationHandler

from .models import User
from .serializers import UserSerializer


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class EmailVerificationAndUserUpdateView(APIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        email_verification_handler = EmailVerificationHandler(
            code=kwargs.get("code"), email=kwargs.get("email")
        )
        email_result, user = email_verification_handler.proccess_email_verification()
        try:
            if email_result:
                request.session["user_id"] = user.id
                return Response({"EmailVerification": user.is_verified_email}, status=status.HTTP_200_OK)
            return Response(
                {"EmailVerification": "EmailVerification is expired or not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception:
            return Response({"EmailVerification": "Произошла ошибка"}, status=status.HTTP_400_BAD_REQUEST)