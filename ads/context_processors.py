from .services import get_ads_for_user

def ads_processor(request):
    qs = get_ads_for_user(request.user)

    return {
        "ads": qs.filter(ad_type="feed")[:3],
        "sidebar_ads": qs.filter(ad_type="sidebar")[:2],
    }
