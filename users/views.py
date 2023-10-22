from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import EmailVerification, User
from .serializers import UserSerializer


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )


class EmailVerificationAndUserUpdateView(APIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        code = kwargs.get('code')
        email = kwargs.get('email')
        user = get_object_or_404(User, email=email)
        email_verifications = EmailVerification.objects.filter(code=code, user=user)
        try:
            if email_verifications.exists() and not email_verifications.last().is_expired():
                user.is_verified_email = True
                user.save()
                self.request.session['user_id'] = user.id
                return Response({'EmailVerification': user.is_verified_email})
            return Response({'EmailVerification': 'EmailVerification is expired or not exists'})
        except Exception:
            return Response({'EmailVerification': 'Произошла ошибка'})
        
    def patch(self, request, *args, **kwargs):
        user_id = request.session.get('user_id', )
        # Проверяем наличие 'first_name' и 'last_name' в данных
        if 'first_name' not in request.data or 'last_name' not in request.data:
            return Response({'message': 'Имя и Фамилия обязательны'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.save()
        return Response({'message': "Имя и Фамилия добавлены"}, status=status.HTTP_200_OK)
