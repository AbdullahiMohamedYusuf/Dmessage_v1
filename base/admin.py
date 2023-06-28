from django.contrib import admin
from .models import Messages, FriendList, Handle
# Register your models here.
admin.site.register(Messages)
admin.site.register(FriendList)
admin.site.register(Handle)