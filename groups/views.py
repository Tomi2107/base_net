from django.views.generic import ListView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from interactions.mixins import SavedByUserMixin

from .models import Group, GroupMember, GroupPost, GroupFollow
from .forms import GroupCreateForm

from .services import request_to_join_group

class GroupListView(LoginRequiredMixin, SavedByUserMixin, ListView):
    model = Group
    template_name = "pages/groups.html"
    context_object_name = "groups"
    model_type = Group

    def get_queryset(self):
        return (
            Group.objects
            .select_related("creator")
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        memberships = GroupMember.objects.filter(user=user)
        membership_map = {
            m.group_id: m for m in memberships
        }

        context["membership_map"] = membership_map
        context["highlight_id"] = self.request.GET.get("highlight")
        context["form"] = GroupCreateForm()

        return context


@login_required
def create_group(request):
    if request.method == "POST":
        form = GroupCreateForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()
            return redirect("groups:list")

    return redirect("groups:list")


@login_required
def group_profile(request, pk):
    group = get_object_or_404(Group, pk=pk)

    membership = GroupMember.objects.filter(
        group=group,
        user=request.user
    ).first()

    is_owner = membership and membership.role == "owner"
    is_admin = membership and membership.role == "admin"
    is_member = membership and membership.status == "approved"
    is_pending = membership and membership.status == "pending"

    is_following = GroupFollow.objects.filter(
        user=request.user,
        group=group
    ).exists()

    context = {
        "group": group,
        "membership": membership,
        "is_owner": is_owner,
        "is_admin": is_admin,
        "is_member": is_member,
        "is_pending": is_pending,
        "is_following": is_following,
    }

    return render(request, "groups/profile.html", context)


@login_required
def group_requests(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # verificar permisos
    if not GroupMember.objects.filter(
        group=group,
        user=request.user,
        role__in=["owner", "admin"],
        status="approved"
    ).exists():
        messages.error(request, "No tenés permisos para ver esto.")
        return redirect("groups:detail", pk=group.id)

    requests = GroupMember.objects.filter(
        group=group,
        status="pending"
    ).select_related("user")

    return render(request, "groups/group_requests.html", {
        "group": group,
        "requests": requests
    })

@login_required
def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # si ya es miembro
    if GroupMember.objects.filter(group=group, user=request.user).exists():
        messages.info(request, "Ya sos miembro o tenés una solicitud pendiente.")
        return redirect("groups:profile", pk=group.id)

    membership, created = request_to_join_group(group, request.user)

    if membership.status == "approved":
        messages.success(request, "Te uniste al grupo 🎉")
    else:
        messages.info(request, "Solicitud enviada. Esperando aprobación 👀")

    return redirect("groups:profile", pk=group.id)

@login_required
def approve_request(request, membership_id):
    membership = get_object_or_404(
        GroupMember,
        id=membership_id,
        status="pending"
    )

    # permisos
    if not GroupMember.objects.filter(
        group=membership.group,
        user=request.user,
        role__in=["owner", "admin"],
        status="approved"
    ).exists():
        messages.error(request, "No tenés permisos.")
        return redirect("groups:profile", group_id=membership.group.id)

    membership.status = "approved"
    membership.save(update_fields=["status"])

    messages.success(request, "Usuario aprobado ✅")
    return redirect("groups:requests", group_id=membership.group.id)

@login_required
def reject_request(request, membership_id):
    membership = get_object_or_404(
        GroupMember,
        id=membership_id,
        status="pending"
    )

    if not GroupMember.objects.filter(
        group=membership.group,
        user=request.user,
        role__in=["owner", "admin"],
        status="approved"
    ).exists():
        messages.error(request, "No tenés permisos.")
        return redirect("groups:detail", group_id=membership.group.id)

    membership.status = "rejected"
    membership.save(update_fields=["status"])

    messages.success(request, "Solicitud rechazada ❌")
    return redirect("groups:requests", group_id=membership.group.id)

@login_required
def create_group_post(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    membership = GroupMember.objects.filter(
        group=group,
        user=request.user,
        status="approved"
    ).first()

    if not membership:
        return redirect("groups:profile", pk=group.id)

    if request.method == "POST":
        body = request.POST.get("body")
        if body:
            GroupPost.objects.create(
                group=group,
                author=request.user,
                body=body
            )

    return redirect("groups:profile", pk=group.id)

@login_required
def leave_group(request, pk):
    membership = get_object_or_404(
        GroupMember,
        group_id=pk,
        user=request.user
    )

    if membership.role == "owner":
        messages.error(request, "El owner no puede salir del grupo.")
        return redirect("groups:profile", pk=pk)

    membership.delete()
    messages.success(request, "Saliste del grupo.")
    return redirect("groups:list")

@login_required
def follow_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    GroupFollow.objects.get_or_create(user=request.user, group=group)
    return redirect('groups:profile', pk=pk)

@login_required
def unfollow_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    GroupFollow.objects.filter(user=request.user, group=group).delete()
    return redirect('groups:profile', pk=pk)
