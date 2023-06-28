from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Messages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.message

class FriendList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")#Everyuser in Users note:remember dropdown
    friends = models.ManyToManyField(User, blank=True, related_name="friends") #List of all your friends

    def __str__(self):
        self.user.username
    
    def add_friend(self, account):
        """
        if user is not in friends list add them 
        function later gets queried by another class "recive"
        """
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()
    
    def unfriend(self, account):
        #if the account is in friends list remove it
        if account in self.friends.all():
            self.friends.remove(account)

class Handle(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")

    is_active = models.BooleanField(blank=True, default=True)


    def accept(self):
        receiver_friend = FriendList.objects.get(user=self.receiver)
        if receiver_friend:
            receiver_friend.add_friend(self.sender)
            sender_friend = FriendList.objects.get(user=self.sender)
            if sender_friend:
                sender_friend.add_friend(self.receiver)
                self.is_active = False
                self.save()
                
    def decline(self):
        self.is_active = False
        self.save()