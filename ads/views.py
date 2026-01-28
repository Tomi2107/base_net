from django.shortcuts import get_object_or_404, redirect, render
from .models import Ad
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import AdForm
from django.contrib.admin.views.decorators import staff_member_required



def ad_click(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)

    ad.clicks += 1
    ad.save(update_fields=["clicks"])
    
    

    return redirect(ad.link)

# ads/views.py


@login_required
def create_ad(request):
    if request.method == "POST":
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.advertiser = request.user
            ad.save()
            form.save_m2m()

            messages.success(
                request,
                "Publicidad creada. Queda pendiente de aprobación 👀"
            )
            return redirect("ads:my_ads")
    else:
        form = AdForm()

    return render(request, "ads/create_ad.html", {
        "form": form
    })

@login_required
def my_ads(request):
    ads = Ad.objects.filter(advertiser=request.user)

    return render(request, "ads/my_ads.html", {
        "ads": ads
    })
    
@login_required
def activate_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk, advertiser=request.user)

    if not ad.approved:
        messages.error(request, "La publicidad aún no fue aprobada.")
        return redirect("ads:my_ads")

    # ACÁ DESPUÉS VA MERCADOPAGO / STRIPE
    ad.active = True
    ad.save()

    messages.success(request, "Publicidad activada correctamente.")
    return redirect("ads:my_ads")

@staff_member_required
def admin_ads_dashboard(request):
    pending = Ad.objects.filter(approved=False)
    active = Ad.objects.filter(active=True)

    return render(request, "ads/admin_dashboard.html", {
        "pending": pending,
        "active": active,
    })

@staff_member_required
def approve_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    ad.approved = True
    ad.save()
    return redirect("ads:admin_dashboard")


@staff_member_required
def reject_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    ad.delete()
    return redirect("ads:admin_dashboard")

