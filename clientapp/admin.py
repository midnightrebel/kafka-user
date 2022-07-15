from django.contrib import admin
from .models import Message, User, TeamLeader, Office
admin.site.register(Message)
admin.site.register(User)
admin.site.register(TeamLeader)
admin.site.register(Office)
# Register your models here.
