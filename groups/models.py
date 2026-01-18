from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Group(models.Model):
    PRIVACY_CHOICES = (
        ("public", "Público"),
        ("private", "Privado"),
    )

    # 🔑 creador del grupo
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_groups"
    )

    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    members_public = models.BooleanField(default=True)

    privacy = models.CharField(
        max_length=10,
        choices=PRIVACY_CHOICES,
        default="public"
    )

    # avatar del grupo
    image = models.ImageField(
        upload_to="groups/images/",
        blank=True,
        null=True
    )

    # portada del grupo
    cover = models.ImageField(
        upload_to="groups/covers/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    # 🔐 helpers de permisos
    def is_owner(self, user):
        return self.memberships.filter(
            user=user,
            role="owner",
            status="approved"
        ).exists()

    def is_admin(self, user):
        return self.memberships.filter(
            user=user,
            role__in=["owner", "admin"],
            status="approved"
        ).exists()

    def is_member(self, user):
        return self.memberships.filter(
            user=user,
            status="approved"
        ).exists()


class GroupMember(models.Model):
    ROLE_CHOICES = (
        ("owner", "Owner"),
        ("admin", "Admin"),
        ("member", "Member"),
    )

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="memberships"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="group_memberships"
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="member"
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending"
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("group", "user")
        ordering = ["joined_at"]

    def __str__(self):
        return f"{self.user} → {self.group} ({self.role} / {self.status})"

    def can_manage(self):
        return self.role in ["owner", "admin"] and self.status == "approved"


class GroupPost(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="group_posts"
    )

    body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Post de {self.author} en {self.group}"
 

class GroupFollow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "group") 