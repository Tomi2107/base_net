# friends/models.py
from django.conf import settings
from django.db import models
from django.db.models import Q

User = settings.AUTH_USER_MODEL

class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User,
        related_name='sent_friend_requests',
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User,
        related_name='received_friend_requests',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(null=True)  
    # None = pendiente | True = aceptada | False = rechazada

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~Q(from_user=models.F('to_user')),
                name='no_self_friend_request'
            ),
            models.UniqueConstraint(
                fields=['from_user', 'to_user'],
                name='unique_friend_request'
            )
        ]

    def __str__(self):
        return f"{self.from_user} → {self.to_user}"

class Friendship(models.Model):
    user1 = models.ForeignKey(
        User,
        related_name='friends_1',
        on_delete=models.CASCADE
    )
    user2 = models.ForeignKey(
        User,
        related_name='friends_2',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user1', 'user2'],
                name='unique_friendship'
            )
        ]

    def save(self, *args, **kwargs):
        # Ordenamos IDs para evitar duplicados inversos
        if self.user1_id > self.user2_id:
            self.user1, self.user2 = self.user2, self.user1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user1} 🤝 {self.user2}"

