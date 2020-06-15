from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth.hashers import make_password

from accounts.models import User
from accounts.serializers import UserSerializer
from shop.models import AdminAccessPermission


class UserViewSet(ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, GenericViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, AdminAccessPermission]

    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-id')


@csrf_exempt
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def user_registration(request):
    serializer = UserSerializer(data=request.POST)

    serializer.is_valid()

    status, answer = serializer.custom_validate()
    if not status:
        return Response(answer)

    serializer.validated_data["password"] = make_password(serializer.validated_data["password"])
    serializer.create(serializer.validated_data)

    del serializer.validated_data["password"]

    return Response(serializer.validated_data)
