import json

from rest_framework import generics
from kafka import KafkaConsumer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import MessageSerializer, UserSerializer
from rest_framework import status
from rest_framework.response import Response
from .models import Message, User


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


class CurrentUserView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication, ]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
