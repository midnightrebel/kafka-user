import json

from rest_framework import generics
from kafka import KafkaConsumer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from .serializers import MessageSerializer, UserSerializer, TeamLeadSerializer, TeamLeadCreate, OfficeSerializer, \
    OfficeCreate
from rest_framework import status
from rest_framework.response import Response
from .models import Message, User, TeamLeader, Office


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
        serializer = TeamLeadCreate(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status.HTTP_201_CREATED)


class CurrentUserView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication, ]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class OfficeListView(viewsets.ModelViewSet):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer

    def create(self, request, *args, **kwargs):
        serializer = OfficeCreate(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status.HTTP_201_CREATED)
