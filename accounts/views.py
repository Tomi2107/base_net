from accounts.forms import EditProfileForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View
from accounts.models import Profile, UserOpinion
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
User = get_user_model()
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader
from django.contrib import messages
from django.http import HttpResponse
from .forms import UserOpinionForm, UserOpinionForm

from django.db.models import Avg
from .models import UserOpinion

from pets.models import Pet
from pets.forms import PetForm

from foster.models import FosterAvailability
from foster.forms import FosterAvailabilityForm

from math import floor
from friends.utils import get_friendship_status

from django.contrib import messages

from ads.services import get_ads_for_user
from ads.models import Ad

    

@login_required
def UserProfileView(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    pets = user.pets.all()

    # 🔹 FRIENDSHIP STATUS (🔥 ESTO FALTABA)
    friendship_status = get_friendship_status(request.user, user)

    followers = profile.followers.all()
    is_following = request.user in followers
    number_of_followers = followers.count()

    lost_pets = pets.filter(status="lost")
    dating_pets = pets.filter(status="dating")

    opinions = UserOpinion.objects.filter(
        profile=profile
    ).order_by("-created")

    has_opinions = opinions.exists()
    average_rating = opinions.aggregate(avg=Avg("rating"))["avg"]
    average_rating_int = int(round(average_rating)) if average_rating else 0

    user_opinion = None
    if request.user != profile.user:
        user_opinion = UserOpinion.objects.filter(
            profile=profile,
            author=request.user
        ).first()

    if request.method == "POST":
        form = UserOpinionForm(
            request.POST,
            instance=user_opinion
        )
        if form.is_valid():
            opinion = form.save(commit=False)
            opinion.profile = profile
            opinion.author = request.user
            opinion.save()
            return redirect("users:profile", username=profile.user.username)
    else:
        form = UserOpinionForm(instance=user_opinion)
        
    friendship_status = get_friendship_status(request.user, user)

    menu = {
        "is_self": request.user == user,
        "is_friend": friendship_status == "friends",
    }
    
    ads = get_ads_for_user(request.user)

    for ad in ads:
        ad.views += 1

    Ad.objects.bulk_update(ads, ["views"])

    context = {
        "profile": profile,
        "profile_user": user,          # ✅ para consistencia
        "pets": pets,
        "lost_pets": lost_pets,
        "dating_pets": dating_pets,
        "number_of_followers": number_of_followers,
        "is_following": is_following,
        "opinions": opinions,
        "average_rating": average_rating,
        "average_rating_int": average_rating_int,
        "has_opinions": has_opinions,
        "form": form,
        "user_opinion": user_opinion,

        # 🔥 AHORA SÍ
        "friendship_status": friendship_status,
        "context_menu": menu,
        "is_self": request.user == user,
        "is_friend": friendship_status == "friends",
        "ads": ads,
    
    }

    return render(request, "users/detail.html", context)




@login_required
def EditProfile(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)
    user_basic_info = User.objects.get(id=user)

    pets = Pet.objects.filter(owner=request.user)
    pet_form = PetForm()

    # 🔹 Foster availability (get or none)
    foster_instance = FosterAvailability.objects.filter(user=request.user).first()
    foster_form = FosterAvailabilityForm(instance=foster_instance)

    if request.method == 'POST':

        # ✅ alta mascota (NO SE TOCA)
        if 'add_pet' in request.POST:
            pet_form = PetForm(request.POST)
            if pet_form.is_valid():
                pet = pet_form.save(commit=False)
                pet.owner = request.user
                pet.save()
                return redirect('users:edit-profile')

        # ✅ NUEVO: Foster form
        if 'save_foster' in request.POST:
            foster_form = FosterAvailabilityForm(
                request.POST,
                instance=foster_instance
            )
            if foster_form.is_valid():
                foster = foster_form.save(commit=False)
                foster.user = request.user
                foster.is_active = True
                foster.save()
                return redirect('users:edit-profile')

        # 🔴 perfil (NO SE TOCA)
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            user_basic_info.first_name = form.cleaned_data.get('first_name')
            user_basic_info.last_name = form.cleaned_data.get('last_name')

            profile.picture = form.cleaned_data.get('picture')
            profile.banner = form.cleaned_data.get('banner')
            profile.location = form.cleaned_data.get('location')
            profile.url = form.cleaned_data.get('url')
            profile.birthday = form.cleaned_data.get('birthday')
            profile.bio = form.cleaned_data.get('bio')

            profile.save()
            user_basic_info.save()
            return redirect('users:profile', username=request.user.username)

    else:
        form = EditProfileForm(instance=profile)

    context = {
        'form': form,
        'pets': pets,
        'pet_form': pet_form,
        'foster_form': foster_form,   # ✅ NUEVO
    }

    return render(request, 'users/edit.html', context)



class AddFollower(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		profile = Profile.objects.get(pk=pk)
		profile.followers.add(request.user)
		messages.add_message(
            self.request,
            messages.SUCCESS,
            'User Followed'
        )
		return redirect('users:profile', username=request.user.username)


class RemoveFollower(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		profile = Profile.objects.get(pk=pk)
		profile.followers.remove(request.user)
		messages.add_message(
            self.request,
            messages.SUCCESS,
            'User Unfollowed'
        )
		return redirect('users:profile', username=request.user.username)


class ListFollowers(View):
    def get(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        followers = profile.followers.all()

        context = {
            'profile': profile,
            'followers': followers
        }

        return render(request, 'pages/social/followers_list.html', context)
    
@login_required
def add_opinion(request, username):
    profile = get_object_or_404(User, username=username)

    if request.method == "POST":
        form = UserOpinionForm(request.POST)
        if form.is_valid():
            opinion = form.save(commit=False)
            opinion.author = request.user
            opinion.profile = profile
            opinion.save()
            return redirect("users:profile", username=username)
    else:
        form = UserOpinionForm()

    return render(request, "users/opinion_form.html", {
        "form": form,
        "profile": profile
    })
    
@login_required
def delete_opinion(request, opinion_id):
    opinion = get_object_or_404(
        UserOpinion,
        id=opinion_id,
        author=request.user
    )

    profile_username = opinion.profile.user.username
    opinion.delete()

    return redirect("users:profile", username=profile_username)    

@login_required
def account_delete(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        messages.success(request, "Tu cuenta ha sido eliminada correctamente.")
        return redirect("landing")  # o 'account_login' si querés ir al login

    return render(request, "account/account_delete_confirm.html")    
