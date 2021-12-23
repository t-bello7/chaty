from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class RoomManager(models.Manager):
    def by_user(self, user):
        qlookup = Q(first=user)  | Q(second=user)
        qlookup2 = Q(first=user) & Q(second=user)
        qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
        return qs

    def get_or_new(self, user, other_username):
        username = user.username
        if username == other_username:
            return None
        qlookup1 = Q(first__username=username) & Q(second__username=other_username)
        qlookup2 = Q(first__username=other_username) & Q(second_username=username)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
        if qs.count() == 1:
            return qs.first(), False
        elif qs.count()> 1:
            return qs.order_by('timestamp').first(), False
        else:
            Klass = user.__class__
            user2 = Klass.objects.get(username=other_username)
            if user != user2:
                obj = self.model(first=user, second=user2)
                obj.save()
                return obj, True
            return None, False



class Room(models.Model):
    title = models.CharField(max_length=255, unique=True, blank=False)
    first_user = models.ForeignKey(User, on_delete=models.CASCADE, default='user1', related_name='user_one')
    second_user = models.ForeignKey(User, on_delete=models.CASCADE, default='user2', related_name='user_two')

    objects = RoomManager()
    def __str__(self):
        return self.title

    @property
    def room_name(self):
        return f"room-{self.id}"
    
    def broadcast(self, msg=None):
        if msg is not None:
            broadcast_msg_to_chat(msg, group_name=self.room_name, user='admin')
            return True
        return False

class RoomMessageManager(models.Manager):
    def by_room(self, room):
        qs = ChatMessage.object.filter(room=room).order_by("-timestamp")
        return qs

class RoomMessage(models.Model):
    """
    Chat message in a room
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(unique=False, blank=False)
    read_receipts = models.BooleanField(default=False)

    objects = RoomMessageManager()
    
    def __str__(self):
        return self.content
