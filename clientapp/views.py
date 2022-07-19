import json

from kafka import KafkaConsumer
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Message, User, TeamLeader, Office
from .serializers import MessageSerializer, UserSerializer, TeamLeadSerializer, OfficeCreateSerializer, \
    UserUpdateSerializer


class ConsumerView(generics.GenericAPIView):
    serializer_class = MessageSerializer
    queryset = User.objects.all()

    def post(self, request):
        payload = ''
        consumer = KafkaConsumer('Ptopic',
                                 bootstrap_servers=['localhost:9092'],
                                 auto_offset_reset='latest'
                                 )
        if consumer.bootstrap_connected():
            for message in consumer:
                payload = json.loads(message.value)
                print(payload)
                userdata = Message.objects.create_message(payload)
        return Response(payload, status.HTTP_200_OK)


class TeamLeadViewSet(viewsets.ViewSet):
    queryset = TeamLeader.objects.all()
    serializer_class = TeamLeadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CurrentUserView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication, ]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AdminChangeView(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = User.objects.prefetch_related('office').select_related('teamleader')
    serializer_class = UserUpdateSerializer


class OfficeViewSet(viewsets.ModelViewSet):
    queryset = Office.objects.all()
    serializer_class = OfficeCreateSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
