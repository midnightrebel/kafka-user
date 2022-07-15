from django.contrib.auth.hashers import check_password
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Message


# @receiver(pre_init,sender=Message)
# def create_message(instance, **kwargs):
#     payload = ''
#     consumer = KafkaConsumer('Ptopic',
#                              bootstrap_servers=['localhost:9092'],
#                              auto_offset_reset='latest'
#                              )
#     if consumer.bootstrap_connected():
#         for message in consumer:
#             payload = json.loads(message.value)
#             userdata = Message.objects.create_message(payload)
#     return Response(payload, status.HTTP_200_OK)

@receiver(post_save, sender=Message)
def create_user(instance, **kwargs):
    values = list(instance.content.values())
    User.objects.create_user(values[1], values[0], values[2])
